import { beforeEach, describe, expect, it, vi } from "vitest";

// R-02: the stored "false" must come back as off after a reload.
function stubStorage(initial: Record<string, string>) {
    const data = new Map(Object.entries(initial));
    vi.stubGlobal("localStorage", {
        getItem: (k: string) => data.get(k) ?? null,
        setItem: (k: string, v: string) => void data.set(k, v),
        removeItem: (k: string) => void data.delete(k),
    });
    return data;
}

async function load() {
    vi.resetModules();
    return (await import("../src/lib/stores/auto-settings-store")).AutoSettings;
}

describe("AutoSettings", () => {
    beforeEach(() => vi.unstubAllGlobals());

    it.each([
        [undefined, false],
        ["false", false],
        ["true", true],
    ])("reads stored %s as %s", async (stored, expected) => {
        stubStorage(stored === undefined ? {} : { auto_forward_enabled: stored });
        expect((await load()).store.state.enabled).toBe(expected);
    });

    it("keeps off after switching on then off and reloading", async () => {
        const data = stubStorage({});
        let auto = await load();
        auto.toggleEnabled();
        auto.toggleEnabled();
        expect(data.get("auto_forward_enabled")).toBe("false");
        auto = await load();
        expect(auto.store.state.enabled).toBe(false);
    });

    it("persists the quick-tools toggle too", async () => {
        const data = stubStorage({});
        (await load()).setEnabled(true);
        expect(data.get("auto_forward_enabled")).toBe("true");
        expect((await load()).store.state.enabled).toBe(true);
    });
});
