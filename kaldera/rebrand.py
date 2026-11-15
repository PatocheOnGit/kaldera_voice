# -*- coding: utf-8 -*-
"""
Kaldera Voice rebrand of the Plasmo Voice sources (applied once on the kaldera branch; kept to redo it after a
merge from upstream if a conflict wiped a change). Every edit checks its anchor and does nothing when already done.

    python kaldera/rebrand.py
"""
import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
MAIN = ROOT / "client/src/main"
KOTLIN = MAIN / "kotlin/su/plo"
JAVA = MAIN / "java/su/plo"


def edit(path, pairs):
    path = Path(path)
    text = path.read_text(encoding="utf-8")
    for old, new in pairs:
        if new in text:
            continue
        if old not in text:
            raise SystemExit(f"{path}: anchor not found: {old[:70]}")
        text = text.replace(old, new, 1)
    path.write_text(text, encoding="utf-8")


# Kaldera palette (docs: site and launcher colours).
edit(KOTLIN / "lib/mod/client/render/Colors.kt", [
    ("val GRAY = Color(0xA0A0A0)", "val GRAY = Color(0x8D8780)"),
    ("val TEXT = Color(0xE0E0E0)", "val TEXT = Color(0xF4EDE6)"),
    ("val TEXT_DISABLED = Color(0x707070)", "val TEXT_DISABLED = Color(0x5E5953)"),
    ("val TEXT_MUTED = Color(0x808080)", "val TEXT_MUTED = Color(0x8D8780)"),
    ("val BACKGROUND = Color(0x404040)", "val BACKGROUND = Color(0x1D1D22)"),
    ("val WARNING = Color(0xFAC653)", "val WARNING = Color(0xE8A33D)"),
])
edit(JAVA / "lib/mod/client/gui/components/TextFieldWidget.java", [
    ("CURSOR_COLOR = new Color(0xD0D0D0)", "CURSOR_COLOR = new Color(0xF4EDE6)"),
    ("HIGHLIGHT_COLOR = new Color(0x4B4BFF)", "HIGHLIGHT_COLOR = new Color(0xE2540C)"),
])
edit(KOTLIN / "lib/mod/client/gui/components/ScrollContainer.kt", [("val THUMB_COLOR = Color(0xC0C0C0)", "val THUMB_COLOR = Color(0xFF8A45)")])
edit(KOTLIN / "voice/client/gui/settings/widget/DropDownWidgetList.kt", [
    ("private val frameColor = Color(0x464646)", "private val frameColor = Color(0x3A3A43)"),
    ("private val hoverColor = Color(0x323232)", "private val hoverColor = Color(0x2A2A31)"),
])
edit(JAVA / "voice/client/gui/settings/widget/ActivationThresholdWidget.java", [
    ("LEVEL_HIGH_COLOR = new Color(0xFF0000)", "LEVEL_HIGH_COLOR = new Color(0xC42340)"),
    ("LEVEL_MEDIUM_COLOR = new Color(0xFFFF00)", "LEVEL_MEDIUM_COLOR = new Color(0xE8A33D)"),
    ("LEVEL_LOW_COLOR = new Color(0x00FF00)", "LEVEL_LOW_COLOR = new Color(0x4ADE80)"),
])

# Name, credits and links: Plasmo Voice stays credited as the original.
edit(JAVA / "voice/client/gui/settings/VoiceSettingsScreen.java", [
    ('                McTextComponent.literal("Plasmo Voice"),', '                McTextComponent.literal("Kaldera Voice"),'),
    ('String.format("Plasmo Voice %s%s Settings"', 'String.format("Kaldera Voice %s%s Settings"'),
])
edit(JAVA / "voice/client/gui/settings/tab/AboutTabWidget.java", [
    ("GRAY_TEXT_COLOR = new Color(0xAAAAAA)", "GRAY_TEXT_COLOR = new Color(0x8D8780)"),
    ('        CompositeColumnWidget linkRows = addCategory(links());\n',
     '        CompositeColumnWidget linkRows = addCategory(links());\n'
     '        // Kaldera Voice: the fork and its source code (LGPL-3.0), then the original project.\n'
     '        linkRows.add(new CompositeRowWidget(\n'
     '                ELEMENT_GAP,\n'
     '                linkButton("Kaldera Voice", "https://github.com/PatocheOnGit/kaldera_voice")\n'
     '        ));\n'),
])
edit(KOTLIN / "voice/client/integration/ClothConfigMenu.kt", [('McTextComponent.literal("Plasmo Voice")', 'McTextComponent.literal("Kaldera Voice")')])

# No call to Plasmo's servers from players' games: updates and texts come with the Kaldera launcher.
edit(JAVA / "voice/client/BaseVoiceClient.java", [
    ("    @EventSubscribe\n    public void onUdpConnected(@NotNull UdpClientConnectedEvent event) {",
     "    // Kaldera Voice: no update check, the Kaldera launcher delivers updates.\n    public void onUdpConnected(@NotNull UdpClientConnectedEvent event) {"),
    ("        if (!config.getDisableCrowdin().value()) {\n            PlasmoCrowdinMod.INSTANCE.downloadTranslations(",
     "        // Kaldera Voice: translations ship with the mod, nothing is downloaded.\n        if (false && !config.getDisableCrowdin().value()) {\n            PlasmoCrowdinMod.INSTANCE.downloadTranslations("),
])
edit(KOTLIN / "voice/client/meta/PlasmoVoiceMeta.kt", [
    ("        fun fetch(languageName: String) {\n            CoroutineScopes.DefaultSupervisor.launch { fetchOrLoadSync(languageName) }\n        }",
     "        fun fetch(languageName: String) {\n            // Kaldera Voice: no request to plasmovoice.com, the built-in credits are used.\n        }"),
])

# Build: no Crowdin download (deterministic builds, only English and the Kaldera French text are shipped).
build_file = ROOT / "client/build.gradle.kts"
build_text = build_file.read_text(encoding="utf-8")
marker = "// Kaldera Voice: no Crowdin download"
if marker not in build_text:
    addition = (marker + " (deterministic builds, English and Kaldera's French only).\n"
                "tasks.matching { it.name == \"crowdinDownload\" }.configureEach { enabled = false }\n")
    build_file.write_text(build_text.rstrip("\n") + "\n\n" + addition, encoding="utf-8")

# Mod metadata.
edit(MAIN / "resources/META-INF/neoforge.mods.toml", [
    ('issueTrackerURL="https://github.com/plasmoapp/plasmo-voice/issues"', 'issueTrackerURL="https://github.com/PatocheOnGit/kaldera_voice/issues"'),
    ('displayName="Plasmo Voice"', 'displayName="Kaldera Voice"'),
    ('displayURL="https://github.com/plasmoapp/plasmo-voice"', 'displayURL="https://github.com/PatocheOnGit/kaldera_voice"'),
    ('authors="Apehum"', 'authors="Apehum and the Plasmo team (Plasmo Voice), Kaldera (fork)"'),
    ('description="A proximity voice chat mod with audio positioning and lots of features"',
     'description="Kaldera\'s proximity voice chat. A modified version of Plasmo Voice by Plasmo, under the LGPL-3.0: https://github.com/plasmoapp/plasmo-voice"'),
])
Image.open(ROOT / "kaldera/logo.png").convert("RGBA").resize((128, 128), Image.LANCZOS).save(MAIN / "resources/icon.png")

# Texts: English brand strings, full French translation (kaldera/fr_fr.json).
lang = MAIN / "resources/assets/plasmovoice/lang"
en = json.loads((lang / "en_us.json").read_text(encoding="utf-8"))
en["key.category.plasmovoice.name"] = "Kaldera Voice"
en["gui.plasmovoice.not_available"] = "Voice chat is not available on this server"
en["gui.plasmovoice.devices.mac_microphone_permission_denied.tooltip"] = en["gui.plasmovoice.devices.mac_microphone_permission_denied.tooltip"].replace("Plasmo Voice", "Kaldera Voice")
en["message.plasmovoice.update_available"] = en["message.plasmovoice.update_available"].replace("Plasmo Voice", "Kaldera Voice")
en["gui.plasmovoice.about.copyright"] = ("Kaldera Voice is a modified version of Plasmo Voice by Plasmo (Apehum and the Plasmo team), "
                                          "under the LGPL-3.0. Source code: github.com/PatocheOnGit/kaldera_voice. Thanks to them.")
en["modmenu.descriptionTranslation.plasmovoice"] = "Kaldera's proximity voice chat, based on Plasmo Voice"
en["modmenu.summaryTranslation.plasmovoice"] = "Kaldera's proximity voice chat, based on Plasmo Voice"
(lang / "en_us.json").write_text(json.dumps(en, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(lang / "fr_fr.json").write_text((ROOT / "kaldera/fr_fr.json").read_text(encoding="utf-8"), encoding="utf-8")
print("Kaldera Voice rebrand applied")
