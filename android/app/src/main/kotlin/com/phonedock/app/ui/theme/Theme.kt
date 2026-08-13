package com.phonedock.app.ui.theme

import android.os.Build
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.dynamicDarkColorScheme
import androidx.compose.material3.dynamicLightColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext

private val DarkColorScheme = darkColorScheme(
    primary = SageGreen,
    onPrimary = ForestGreen,
    secondary = SandYellow,
    background = Color(0xFF111111),
    surface = Color(0xFF1C1C1E), // Apple-style dark surface
    onSurface = Color(0xFFFBFBFA),
    onSurfaceVariant = MutedGray,
    outline = BorderGray
)

private val LightColorScheme = lightColorScheme(
    primary = ForestGreen,
    onPrimary = Color.White,
    primaryContainer = SageGreen,
    onPrimaryContainer = ForestGreen,
    secondary = GoldBrown,
    secondaryContainer = SandYellow,
    onSecondaryContainer = GoldBrown,
    background = Bone,
    surface = Color.White,
    onSurface = OffBlack,
    onSurfaceVariant = MutedGray,
    outline = BorderGray
)

@Composable
fun PhoneDockTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    // Set dynamicColor to false by default to prioritize our Natural Tones
    dynamicColor: Boolean = false,
    content: @Composable () -> Unit
) {
    val colorScheme = when {
        dynamicColor && Build.VERSION.SDK_INT >= Build.VERSION_CODES.S -> {
            val context = LocalContext.current
            if (darkTheme) dynamicDarkColorScheme(context) else dynamicLightColorScheme(context)
        }

        darkTheme -> DarkColorScheme
        else -> LightColorScheme
    }

    MaterialTheme(
        colorScheme = colorScheme,
        typography = Typography,
        content = content
    )
}
