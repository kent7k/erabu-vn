import Character from "@/models/Character";
import { RegisteredCharacters } from "@drincs/pixi-vn";

// 登場人物（P2）。立ち絵は先輩だけで、ほかは声だけ（物差し＝立ち絵 1 人）。絵は P3 で決め直す。
export const mc = new Character("mc", {
    name: "わたし",
});

export const senpai = new Character("senpai", {
    name: "先輩",
    color: "#0084ac",
});

export const kaikei = new Character("kaikei", {
    name: "会計の子",
});

export const mio = new Character("mio", {
    name: "みお",
});

export const shisho = new Character("shisho", {
    name: "司書さん",
});

RegisteredCharacters.add([mc, senpai, kaikei, mio, shisho]);
