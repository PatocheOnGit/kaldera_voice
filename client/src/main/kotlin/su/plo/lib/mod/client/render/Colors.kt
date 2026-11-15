package su.plo.lib.mod.client.render

import java.awt.Color

object Colors {
    @JvmField
    val WHITE = Color.WHITE
    @JvmField
    val BLACK = Color.BLACK
    @JvmField
    val GRAY = Color(0x8D8780)

    @JvmField
    val TEXT = Color(0xF4EDE6)
    @JvmField
    val TEXT_DISABLED = Color(0x5E5953)
    @JvmField
    val TEXT_MUTED = Color(0x8D8780)
    @JvmField
    val BACKGROUND = Color(0x1D1D22)
    @JvmField
    val WARNING = Color(0xE8A33D)

    @JvmStatic
    fun Color.withAlpha(alpha: Int): Color =
        Color(red, green, blue, alpha)

    @JvmStatic
    fun Color.withAlpha(alpha: Float): Color =
        Color(red, green, blue, (alpha * 255f).toInt())

    @JvmStatic
    operator fun Color.times(scalar: Double): Color =
        Color(
            (red * scalar).toInt().coerceIn(0, 255),
            (green * scalar).toInt().coerceIn(0, 255),
            (blue * scalar).toInt().coerceIn(0, 255),
            alpha
        )
}
