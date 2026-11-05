import { TextReplaces } from "@drincs/pixi-vn-ink";
import { RegisteredCharacters } from "@drincs/pixi-vn/characters";

TextReplaces.add((key) => RegisteredCharacters.get(key)?.name, {
    name: "character name",
    validation: "characterId",
    type: "after-translation",
    i18nInterpolation: true,
    description: "Replaces a character ID with the character's name in the game.",
});
