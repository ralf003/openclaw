// Empty allowlist policy tests cover doctor policy behavior when allowlists are empty.
import { describe, expect, it, vi } from "vitest";
import { collectEmptyAllowlistPolicyWarningsForAccount } from "./empty-allowlist-policy.js";

vi.mock("../channel-capabilities.js", () => ({
  getDoctorChannelCapabilities: (channelName?: string) => ({
    dmAllowFromMode: "topOnly",
    groupModel: channelName === "discord" ? "route" : "sender",
    groupAllowFromFallbackToAllowFrom: channelName !== "imessage",
    warnOnEmptyGroupSenderAllowlist: channelName !== "discord",
  }),
  resolveDoctorChannelAccountIds: () => undefined,
}));

vi.mock("./channel-doctor.js", () => ({
  shouldSkipChannelDoctorDefaultEmptyGroupAllowlistWarning: ({
    channelName,
  }: {
    channelName?: string;
  }) => channelName === "zalouser",
}));

describe("doctor empty allowlist policy warnings", () => {
  it("warns when dm allowlist mode has no allowFrom entries", () => {
    const warnings = collectEmptyAllowlistPolicyWarningsForAccount({
      account: { dmPolicy: "allowlist" },
      channelName: "signal",
      doctorFixCommand: "openclaw doctor --fix",
      prefix: "channels.signal",
    e: "zalouser",
      doctorFixCommand: "openclaw doctor --fix",
      prefix: "channels.zalouser",
    });

    expect(warnings).toStrictEqual([]);
  });

  it("stays quiet for channels that do not use sender-based group allowlists", () => {
    const warnings = collectEmptyAllowlistPolicyWarningsForAccount({
      account: { groupPolicy: "allowlist" },
      channelName: "discord",
      doctorFixCommand: "openclaw doctor --fix",
      prefix: "channels.discord",
    });

    expect(warnings).toStrictEqual([]);
  });
});
