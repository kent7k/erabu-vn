import { readdirSync, readFileSync } from "node:fs";
import { join } from "node:path";
import { convertInkToJson } from "@drincs/pixi-vn-ink/converter";
import { describe, expect, it } from "vitest";

/**
 * 脚本の網羅 — エンジン（pixi-vn-ink の変換器）が ink をどう理解したかを、label の図として歩く。
 * 確かめること: 全部の .ink が変換できる／参照先の label が全部ある／start からの全経路が明示の END で終わる／
 * ending_ で始まる knot が全部どこかの経路で届く／エンドが 2 つ以上・2 択以上の分岐が 1 つ以上（計画の物差し）。
 */

type Step = Record<string, unknown>;
type Labels = Record<string, Step[]>;
type Frame = { label: string; i: number };
type Path = { ending: string | null; trail: string[] };

const INK_DIR = join(import.meta.dirname, "..", "ink");
const ASSETS_DIR = join(import.meta.dirname, "..", "src", "assets");
const START = "start";
const ENDING_PREFIX = "ending_";
const MAX_PATHS = 10_000;
const MAX_STEPS_PER_PATH = 5_000;
/** 歩き方を知っている step の鍵。条件分岐など新しい形が出たら直線として黙って通さず、落として歩き方を足させる。 */
const KNOWN_STEP_KEYS = new Set([
    "choices",
    "dialogue",
    "end",
    "glueEnabled",
    "goNextStep",
    "labelToOpen",
    "operations",
]);

function loadLabels(): Labels {
    const labels: Labels = {};
    for (const file of readdirSync(INK_DIR).filter((f) => f.endsWith(".ink"))) {
        const json = convertInkToJson(readFileSync(join(INK_DIR, file), "utf8"));
        if (!json?.labels) throw new Error(`${file}: 変換できない`);
        for (const [name, steps] of Object.entries(json.labels)) {
            if (labels[name]) throw new Error(`label ${name} が 2 か所にある（${file}）`);
            labels[name] = steps as Step[];
        }
    }
    return labels;
}

/** knot の名前（選択肢の枝 `knot_|_c-0` は親の knot に畳む）。 */
const knotOf = (label: string) => label.split("_|_")[0];

type LabelRef = { label: string; type: string };

function refsOf(step: Step): LabelRef[] {
    const refs: LabelRef[] = [];
    const open = step.labelToOpen as LabelRef | LabelRef[] | undefined;
    if (open) refs.push(...(Array.isArray(open) ? open : [open]));
    for (const c of (step.choices as LabelRef[] | undefined) ?? []) refs.push(c);
    return refs;
}

function walk(labels: Labels): { paths: Path[]; choicePoints: number[] } {
    const paths: Path[] = [];
    const choicePoints: number[] = [];
    const stack: { frames: Frame[]; trail: string[]; steps: number }[] = [
        { frames: [{ label: START, i: 0 }], trail: [START], steps: 0 },
    ];
    for (let cur = stack.pop(); cur; cur = stack.pop()) {
        if (paths.length > MAX_PATHS) throw new Error("経路が多すぎる（輪になっていないか）");
        let { frames } = cur;
        const { trail } = cur;
        for (let n = cur.steps; ; n++) {
            if (n > MAX_STEPS_PER_PATH) throw new Error(`終わらない経路: ${trail.join(" → ")}`);
            const top = frames.at(-1);
            if (!top) {
                paths.push({ ending: null, trail });
                break;
            }
            const steps = labels[top.label];
            if (!steps) throw new Error(`無い label へ飛んだ: ${top.label}`);
            if (top.i >= steps.length) {
                frames = frames.slice(0, -1);
                continue;
            }
            const step = steps[top.i];
            const unknown = Object.keys(step).filter((k) => !KNOWN_STEP_KEYS.has(k));
            if (unknown.length)
                throw new Error(
                    `知らない step の形 ${unknown.join(",")}（${top.label}）— 歩き方を足す`,
                );
            const next = [...frames.slice(0, -1), { ...top, i: top.i + 1 }];
            if ("end" in step) {
                paths.push({ ending: knotOf(top.label), trail });
                break;
            }
            const choices = step.choices as LabelRef[] | undefined;
            if (choices?.length) {
                choicePoints.push(choices.length);
                for (const c of choices) {
                    const frames2 =
                        c.type === "jump"
                            ? [...frames.slice(0, -1), { label: c.label, i: 0 }]
                            : [...next, { label: c.label, i: 0 }];
                    stack.push({ frames: frames2, trail: [...trail, c.label], steps: n + 1 });
                }
                break;
            }
            const open = step.labelToOpen as LabelRef | LabelRef[] | undefined;
            const opens = open ? (Array.isArray(open) ? open : [open]) : [];
            if (opens.length > 1)
                throw new Error(`1 つの step に label が 2 つ以上（${top.label}）— 歩き方を足す`);
            if (opens[0]?.type === "jump") {
                frames = [...frames.slice(0, -1), { label: opens[0].label, i: 0 }];
                trail.push(opens[0].label);
            } else if (opens[0]) {
                frames = [...next, { label: opens[0].label, i: 0 }];
                trail.push(opens[0].label);
            } else {
                frames = next;
            }
        }
    }
    return { paths, choicePoints };
}

describe("脚本の網羅（ink → pixi-vn の label の図）", () => {
    const labels = loadLabels();
    const { paths, choicePoints } = walk(labels);
    const endings = new Set(paths.map((p) => p.ending));

    it("参照先の label が全部ある", () => {
        const missing = Object.values(labels)
            .flatMap((steps) => steps.flatMap(refsOf))
            .map((r) => r.label)
            .filter((l) => !labels[l]);
        expect(missing).toEqual([]);
    });

    it("start からの全経路が明示の END で終わる（尻切れが無い）", () => {
        const dangling = paths.filter((p) => p.ending === null).map((p) => p.trail.join(" → "));
        expect(dangling).toEqual([]);
    });

    it("ending_ の knot が全部どこかの経路で届く", () => {
        const declared = Object.keys(labels)
            .map(knotOf)
            .filter((k) => k.startsWith(ENDING_PREFIX));
        const unreached = [...new Set(declared)].filter((k) => !endings.has(k));
        expect(unreached).toEqual([]);
    });

    it("エンドが 2 つ以上・2 択以上の分岐が 1 つ以上ある（計画の物差し）", () => {
        expect(
            [...endings].filter((e) => e?.startsWith(ENDING_PREFIX)).length,
        ).toBeGreaterThanOrEqual(2);
        expect(choicePoints.some((n) => n >= 2)).toBe(true);
    });

    it("脚本が指す絵と音が全部 src/assets にある（テンプレの外の URL を指さない）", () => {
        const aliases = new Set<string>();
        const bundles = new Set<string>();
        for (const dir of readdirSync(ASSETS_DIR, { withFileTypes: true }).filter((d) =>
            d.isDirectory(),
        )) {
            bundles.add(dir.name);
            for (const file of readdirSync(join(ASSETS_DIR, dir.name))) {
                const base = file.replace(/\.[^.]+$/, "");
                aliases.add(base);
                aliases.add(`${dir.name}_${base}`);
            }
        }
        const missing: string[] = [];
        for (const file of readdirSync(INK_DIR).filter((f) => f.endsWith(".ink"))) {
            const ink = readFileSync(join(INK_DIR, file), "utf-8");
            for (const [, id] of ink.matchAll(/^# show image bg (\S+)/gm))
                if (!aliases.has(id)) missing.push(id);
            for (const [, ids] of ink.matchAll(/^# show imagecontainer \S+ \[([^\]]+)\]/gm)) {
                for (const id of ids.split(/\s+/)) if (!aliases.has(id)) missing.push(id);
            }
            for (const [, id] of ink.matchAll(/^# (?:play|stop) sound (\S+)/gm))
                if (!aliases.has(id)) missing.push(id);
            for (const [, id] of ink.matchAll(/^# lazyload bundle (\S+)/gm))
                if (!bundles.has(id)) missing.push(id);
        }
        expect(missing).toEqual([]);
        expect(readFileSync(join(ASSETS_DIR, "index.ts"), "utf-8")).not.toMatch(
            /src:\s*["']https?:/,
        );
    });

    it("日本語の文言が英語の文言と同じ鍵を全部持っている（足りないと英語の鍵のまま画面に出る）", () => {
        const keys = (name: string) =>
            Object.keys(
                JSON.parse(readFileSync(join(ASSETS_DIR, "..", "locales", `${name}.json`), "utf-8"))
                    .ui,
            ).sort();
        expect(keys("ja")).toEqual(keys("en"));
    });
});
