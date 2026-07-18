"""
Manually apply PR #95739 changes to a clean upstream/main base.
This avoids the rebase problem where old commits revert new refactoring.
"""
import subprocess
import sys
import os
import shutil

REPO = r"D:\project\openclaw-dev"
TARGET_BRANCH = "feature/memory-search-exclude-paths-v2"

def git(*args, check=True):
    result = subprocess.run(
        ["git", "-C", REPO] + list(args),
        capture_output=True, text=True, encoding='utf-8', errors='replace'
    )
    if check and result.returncode != 0:
        print(f"GIT ERROR: {' '.join(args)}")
        print(result.stderr)
        sys.exit(1)
    return result

def read_file(path):
    with open(os.path.join(REPO, path), 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    full = os.path.join(REPO, path)
    with open(full, 'w', encoding='utf-8', newline='') as f:
        f.write(content)

def apply_edit(path, search, replace):
    """Replace exact search text with replace text in file"""
    content = read_file(path)
    if search not in content:
        print(f"WARNING: search text not found in {path}")
        print(f"  Search: {search[:100]}...")
        return False
    content = content.replace(search, replace, 1)
    write_file(path, content)
    print(f"  Applied edit to {path}")
    return True

# 1. Clean start
print("=== Step 1: Clean start ===")
git("checkout", "upstream/main", "-b", TARGET_BRANCH)

# 2. src/config/types.tools.ts - add excludePaths field
print("\n=== Step 2: types.tools.ts ===")
apply_edit(
    "src/config/types.tools.ts",
    """  /** Extra paths to include in memory search (directories or .md files). */
  extraPaths?: string[];""",
    """  /** Extra paths to include in memory search (directories or .md files). */
  extraPaths?: string[];
  /** Optional glob patterns or exact paths (workspace-relative from memory/) to exclude from memory search indexing.
   *  Supports minimatch-style wildcards.  Applied against workspace-relative paths inside memory/ and extraPaths.
   *  Example: ["memory/dreaming/light", "memory/archive/**"] */
  excludePaths?: string[];"""
)

# 3. src/config/zod-schema.agent-runtime.ts - add zod validation
print("\n=== Step 3: zod-schema.agent-runtime.ts ===")
apply_edit(
    "src/config/zod-schema.agent-runtime.ts",
    "extraPaths: z.array(z.string()).optional(),",
    """extraPaths: z.array(z.string()).optional(),
            excludePaths: z.array(z.string()).optional(),"""
)

# 4. src/config/schema.labels.ts - add label
print("\n=== Step 4: schema.labels.ts ===")
apply_edit(
    "src/config/schema.labels.ts",
    """"agents.defaults.memorySearch.extraPaths": "Extra memory paths",""",
    """"agents.defaults.memorySearch.extraPaths": "Extra memory paths",
  "agents.defaults.memorySearch.excludePaths": "Exclude paths from memory search","""
)

# 5. src/config/schema.help.models.ts - add help text (NOT schema.help.ts which was refactored!)
print("\n=== Step 5: schema.help.models.ts ===")
apply_edit(
    "src/config/schema.help.models.ts",
    """  "agents.defaults.memorySearch.extraPaths":
    "Adds extra directories or .md files to the memory index beyond default memory files. Paths are workspace-relative and support directories plus individual .md files.",\n""",
    """  "agents.defaults.memorySearch.extraPaths":
    "Adds extra directories or .md files to the memory index beyond default memory files. Paths are workspace-relative and support directories plus individual .md files.",
  "agents.defaults.memorySearch.excludePaths":
    "Optional glob patterns or exact paths to exclude from memory search indexing. Supports minimatch wildcards (e.g. memory/dreaming/light). Applied against workspace-relative paths inside memory/ and extraPaths, after built-in auxiliary-path filtering.",
"""
)

# 6. src/config/schema.help.quality.test.ts - add quality check
print("\n=== Step 6: schema.help.quality.test.ts ===")
apply_edit(
    "src/config/schema.help.quality.test.ts",
    """"agents.defaults.memorySearch.extraPaths",""",
    """"agents.defaults.memorySearch.extraPaths",
    "agents.defaults.memorySearch.excludePaths","""
)

# 7. src/agents/memory-search.ts - resolve excludePaths in mergeConfig
print("\n=== Step 7: memory-search.ts ===")
apply_edit(
    "src/agents/memory-search.ts",
    """  const extraPaths = forceStringArray(
    mergeOpt(
      base?.extraPaths,
      overlay?.extraPaths,
    ),
  );""",
    """  const extraPaths = forceStringArray(
    mergeOpt(
      base?.extraPaths,
      overlay?.extraPaths,
    ),
  );
  const excludePaths = forceStringArray(
    mergeOpt(
      base?.excludePaths,
      overlay?.excludePaths,
    ),
  );"""
)

# Also add excludePaths to the return value
apply_edit(
    "src/agents/memory-search.ts",
    """    extraPaths,\n    qmd: mergeOpt(base?.qmd, overlay?.qmd),""",
    """    extraPaths,
    excludePaths,
    qmd: mergeOpt(base?.qmd, overlay?.qmd),"""
)

# 8. extensions/memory-core/src/memory/manager-source-sync-ops.ts - pass excludePaths
print("\n=== Step 8: manager-source-sync-ops.ts ===")
content = read_file("extensions/memory-core/src/memory/manager-source-sync-ops.ts")
# Find the listMemoryFiles call and add excludePaths
old_call = """    const files = await listMemoryFiles(
      this.workspaceDir,
      this.settings.extraPaths,
      this.settings.multimodal,
    );"""
if old_call in content:
    new_call = """    const files = await listMemoryFiles(
      this.workspaceDir,
      this.settings.extraPaths,
      this.settings.multimodal,
      this.settings.excludePaths,
    );"""
    content = content.replace(old_call, new_call, 1)
    write_file("extensions/memory-core/src/memory/manager-source-sync-ops.ts", content)
    print("  Applied edit to manager-source-sync-ops.ts")
else:
    print("  WARNING: listMemoryFiles call not found!")
    # Try to find it
    for i, line in enumerate(content.split('\n'), 1):
        if 'listMemoryFiles' in line:
            print(f"  found at line {i}: {line.strip()}")

# 9. packages/memory-host-sdk/src/host/internal.ts - add isExcludedPath filter
print("\n=== Step 9: host/internal.ts ===")
content = read_file("packages/memory-host-sdk/src/host/internal.ts")

# Add minimatch import
if 'from "minimatch"' not in content:
    for import_line in content.split('\n'):
        if import_line.startswith('import ') and 'from' in import_line:
            last_import_end = content.rfind(import_line) + len(import_line)
    content = content.replace(
        'import { minimatch } from "minimatch";\n',
        ''
    )
    # Find the import block and add
    lines = content.split('\n')
    new_lines = []
    added_minimatch = False
    for i, line in enumerate(lines):
        new_lines.append(line)
        if not added_minimatch and line.startswith('import ') and 'from' in line and i > 5:
            # Check if next line is empty or not an import
            if i+1 < len(lines) and not lines[i+1].startswith('import '):
                new_lines.append('import { minimatch } from "minimatch";')
                added_minimatch = True
    content = '\n'.join(new_lines)
    write_file("packages/memory-host-sdk/src/host/internal.ts", content)
    print("  Added minimatch import")

# Add isExcludedPath helper
helper_code = """
function isExcludedPath(
  relPath: string,
  excludePaths: string[] | undefined,
): boolean {
  if (!excludePaths || excludePaths.length === 0) return false;
  return excludePaths.some((pattern) => {
    // Exact prefix match for plain directory paths (no glob chars)
    if (!/[?*[]/.test(pattern)) {
      return relPath === pattern || relPath.startsWith(pattern + "/");
    }
    // Glob match
    return minimatch(relPath, pattern, { matchBase: false });
  });
}
"""
if 'function isExcludedPath' not in content:
    content = read_file("packages/memory-host-sdk/src/host/internal.ts")
    # Insert after normalizeExtraMemoryPaths
    insert_after = 'function normalizeExtraMemoryPaths'
    func_start = content.index(insert_after)
    # Find the closing brace of this function
    brace_count = 0
    started = False
    insert_pos = func_start
    for i in range(func_start, len(content)):
        if content[i] == '{':
            brace_count += 1
            started = True
        elif content[i] == '}':
            brace_count -= 1
            if started and brace_count == 0:
                insert_pos = i + 1
                break
    # Find next newline
    while insert_pos < len(content) and content[insert_pos] in '\r\n':
        insert_pos += 1
    content = content[:insert_pos] + '\n' + helper_code + '\n' + content[insert_pos:]
    write_file("packages/memory-host-sdk/src/host/internal.ts", content)
    print("  Added isExcludedPath helper")

# Add excludePaths parameter to listMemoryFiles
print("  Updating listMemoryFiles signature...")
content = read_file("packages/memory-host-sdk/src/host/internal.ts")
# Find the function signature
old_sig = "export async function listMemoryFiles(\n  workspaceDir: string,\n  extraPaths?: string[],\n  multimodalHost?: boolean,\n): Promise<MemoryFile[]> {"
new_sig = "export async function listMemoryFiles(\n  workspaceDir: string,\n  extraPaths?: string[],\n  multimodalHost?: boolean,\n  excludePaths?: string[],\n): Promise<MemoryFile[]> {"
if old_sig in content:
    content = content.replace(old_sig, new_sig, 1)
    write_file("packages/memory-host-sdk/src/host/internal.ts", content)
    print("  Updated listMemoryFiles signature")
else:
    print("  WARNING: listMemoryFiles signature not found exactly!")
    # Try to find it
    for i, line in enumerate(content.split('\n'), 1):
        if 'export async function listMemoryFiles' in line:
            print(f"  found at line {i}")

# Add filtering logic in listMemoryFiles body
# Find the dedup section and add exclude filter before it
content = read_file("packages/memory-host-sdk/src/host/internal.ts")
filter_block = """  // Apply excludePaths filtering
  if (excludePaths && excludePaths.length > 0) {
    result = result.filter((f) => !isExcludedPath(f.relativePath, excludePaths));
  }

"""
dedup_marker = "  // Deduplicate by relativePath, keeping first occurrence"
if dedup_marker in content:
    content = content.replace(dedup_marker, filter_block + dedup_marker)
    write_file("packages/memory-host-sdk/src/host/internal.ts", content)
    print("  Added excludePaths filtering logic")
else:
    print("  WARNING: dedup marker not found!")

# 10. packages/memory-host-sdk/src/host/internal.test.ts - add tests
print("\n=== Step 10: host/internal.test.ts ===")
test_code = """
describe("excludePaths", () => {
  it("excludes files matching exact path", async () => {
    const files = await listMemoryFiles(tmpdir, undefined, undefined, [
      "MEMORY.md",
    ]);
    expect(files.map((f) => f.relativePath)).not.toContain("MEMORY.md");
  });

  it("excludes files under a plain directory prefix", async () => {
    const subdir = path.join(tmpdir, "sub");
    fs.mkdirSync(subdir);
    fs.writeFileSync(path.join(subdir, "a.md"), "content a");
    const files = await listMemoryFiles(tmpdir, undefined, undefined, [
      "sub",
    ]);
    const paths = files.map((f) => f.relativePath);
    expect(paths).not.toContain("sub/a.md");
  });

  it("excludes files matching glob wildcard", async () => {
    const archiveDir = path.join(tmpdir, "archive");
    fs.mkdirSync(archiveDir);
    fs.writeFileSync(path.join(archiveDir, "old.md"), "old");
    const files = await listMemoryFiles(tmpdir, undefined, undefined, [
      "archive/**",
    ]);
    const paths = files.map((f) => f.relativePath);
    expect(paths).not.toContain("archive/old.md");
  });

  it("retains non-excluded files alongside excluded ones", async () => {
    const keepFile = path.join(tmpdir, "keep.md");
    fs.writeFileSync(keepFile, "keep");
    const files = await listMemoryFiles(tmpdir, undefined, undefined, [
      "MEMORY.md",
    ]);
    const paths = files.map((f) => f.relativePath);
    expect(paths).toContain("keep.md");
    expect(paths).not.toContain("MEMORY.md");
  });

  it("empty excludePaths retains all files", async () => {
    const files = await listMemoryFiles(tmpdir, undefined, undefined, []);
    const paths = files.map((f) => f.relativePath);
    expect(paths).toContain("MEMORY.md");
  });

  it("no excludePaths parameter retains all files", async () => {
    const files = await listMemoryFiles(tmpdir);
    const paths = files.map((f) => f.relativePath);
    expect(paths).toContain("MEMORY.md");
  });
});
"""
content = read_file("packages/memory-host-sdk/src/host/internal.test.ts")
# Add before the closing "});" of the main describe block
# Find the last "});" which closes the main describe
last_close = content.rfind("});")
content = content[:last_close] + test_code + "\n" + content[last_close:]
write_file("packages/memory-host-sdk/src/host/internal.test.ts", content)
print("  Added excludePaths tests")

# 11. docs/reference/memory-config.md - add docs
print("\n=== Step 11: memory-config.md ===")
apply_edit(
    "docs/reference/memory-config.md",
    """**`extraPaths`** (string[]) — Extra directories or `.md` files to include in the memory index beyond the default `memory/` directory.  Paths are workspace-relative (e.g. `"MyNotes"` or `"MyNotes/summary.md"`).""",
    """**`extraPaths`** (string[]) — Extra directories or `.md` files to include in the memory index beyond the default `memory/` directory.  Paths are workspace-relative (e.g. `"MyNotes"` or `"MyNotes/summary.md"`).

**`excludePaths`** (string[]) — Optional glob patterns or exact paths (workspace-relative from `memory/`) to exclude from memory search indexing.  Supports [minimatch](https://github.com/isaacs/minimatch)-style wildcards.  Applied against workspace-relative paths inside `memory/` and `extraPaths`, after built-in auxiliary-path filtering.  Example: `["memory/dreaming/light", "memory/archive/**"]`"""
)

# 12. extensions/memory-core/src/memory/manager-reindex-state.ts - thread excludePaths
print("\n=== Step 12: manager-reindex-state.ts ===")
apply_edit(
    "extensions/memory-core/src/memory/manager-reindex-state.ts",
    """export function resolveConfiguredScopeHash(params: {
  workspaceDir: string;
  extraPaths?: string[];
  multimodal?: boolean;
}): string {""",
    """export function resolveConfiguredScopeHash(params: {
  workspaceDir: string;
  extraPaths?: string[];
  multimodal?: boolean;
  excludePaths?: string[];
}): string {"""
)

# Add excludePaths to the hash computation
apply_edit(
    "extensions/memory-core/src/memory/manager-reindex-state.ts",
    """  const base = [
    normalizePath(params.workspaceDir),
    ...forceStringArray(params.extraPaths).map(normalizePath).sort(),
    params.multimodal ? "1" : "0",
  ].join("::");""",
    """  const base = [
    normalizePath(params.workspaceDir),
    ...forceStringArray(params.extraPaths).map(normalizePath).sort(),
    params.multimodal ? "1" : "0",
    ...forceStringArray(params.excludePaths).map(normalizePath).sort(),
  ].join("::");"""
)

# 13. manager-sync-ops.ts - thread excludePaths through resolveConfiguredScopeHash calls
print("\n=== Step 13: manager-sync-ops.ts - thread excludePaths ===")
content = read_file("extensions/memory-core/src/memory/manager-sync-ops.ts")
# Find resolveConfiguredScopeHash calls and add excludePaths
# There should be call sites that pass workspaceDir, extraPaths, multimodal
updated = False
for search_call in [
    "resolveConfiguredScopeHash({",
]:
    start = 0
    while True:
        idx = content.find(search_call, start)
        if idx == -1:
            break
        # Find the closing })
        close_idx = content.find("})", idx)
        if close_idx == -1:
            break
        call_block = content[idx:close_idx+2]
        if "excludePaths" not in call_block and "this.settings" in content[max(0,idx-50):idx]:
            # This is a call site we need to update
            # Find multimodal line and add excludePaths after it
            multimodal_idx = call_block.find("multimodal")
            if multimodal_idx != -1:
                # Find the end of the multimodal parameter
                multimodal_end = call_block.find("\n", multimodal_idx)
                if multimodal_end == -1:
                    multimodal_end = call_block.find(",", multimodal_idx)
                if multimodal_end != -1:
                    insert_pos = idx + multimodal_end
                    # Find next non-whitespace
                    nl = content.find('\n', insert_pos)
                    if nl != -1 and nl < close_idx:
                        content = content[:nl+1] + "      this.settings.excludePaths,\n" + content[nl+1:]
                        updated = True
        start = close_idx + 2

if updated:
    write_file("extensions/memory-core/src/memory/manager-sync-ops.ts", content)
    print("  Updated resolveConfiguredScopeHash calls")
else:
    print("  WARNING: no resolveConfiguredScopeHash calls found to update")

# 14. manager-source-sync-ops.ts - also thread excludePaths
print("\n=== Step 14: manager-source-sync-ops.ts - thread excludePaths ===")
content = read_file("extensions/memory-core/src/memory/manager-source-sync-ops.ts")
# Find all resolveConfiguredScopeHash calls and add excludePaths
start = 0
updated = False
while True:
    idx = content.find("resolveConfiguredScopeHash({", start)
    if idx == -1:
        break
    close_idx = content.find("})", idx)
    if close_idx == -1:
        break
    call_block = content[idx:close_idx+2]
    if "excludePaths" not in call_block:
        multimodal_idx = call_block.find("multimodal")
        if multimodal_idx != -1:
            multimodal_end = call_block.find("\n", multimodal_idx)
            if multimodal_end == -1:
                multimodal_end = call_block.find(",", multimodal_idx)
            if multimodal_end != -1:
                insert_pos = idx + multimodal_end
                nl = content.find('\n', insert_pos)
                if nl != -1 and nl < close_idx:
                    content = content[:nl+1] + "      this.settings.excludePaths,\n" + content[nl+1:]
                    updated = True
    start = close_idx + 2

if updated:
    write_file("extensions/memory-core/src/memory/manager-source-sync-ops.ts", content)
    print("  Updated resolveConfiguredScopeHash calls")
else:
    print("  WARNING: no resolveConfiguredScopeHash calls found to update")

# 15. Commit everything
print("\n=== Step 15: Commit ===")
git("add", "-A")
git("commit", "-m", "feat(memory): add excludePaths option to memorySearch config")

print("\n=== Done ===")
git("log", "--oneline", "-3")
