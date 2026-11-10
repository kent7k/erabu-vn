import { beforeEach, describe, expect, it } from "vitest";
import { SearchParams } from "../src/lib/stores/search-param-store";

// R-27: a link with ?utm_source=... must not count as an open menu.
describe("SearchParams.setMany", () => {
    beforeEach(() => SearchParams.store.setState(() => ({})));

    it("ignores params the game does not own", () => {
        SearchParams.setMany({ utm_source: "x", fbclid: "abc" });
        expect(SearchParams.store.state).toEqual({});
    });

    it("keeps the menu params", () => {
        SearchParams.setMany({ settings: true, settings_tab: "saves", utm_source: "x" });
        expect(SearchParams.store.state).toEqual({ settings: true, settings_tab: "saves" });
    });
});
