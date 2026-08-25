package com.phonedock.app.ui.onboarding

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.drawscope.Stroke
import com.phonedock.app.ui.theme.HarvstCoral
import com.phonedock.app.ui.theme.HarvstDarkGreen
import com.phonedock.app.ui.theme.HarvstMutedGreen
import com.phonedock.app.ui.theme.HarvstTan

@Composable
fun IllustrationContainer(
    modifier: Modifier = Modifier,
    content: @Composable () -> Unit
) {
    Box(
        modifier = modifier
            .fillMaxSize()
            .aspectRatio(1f)
    ) {
        content()
    }
}

@Composable
fun PhoneComputerMergeIllustration(modifier: Modifier = Modifier) {
    Canvas(modifier = modifier.fillMaxSize()) {
        val w = size.width
        val h = size.height
        
        // Monitor Silhouette
        drawRoundRect(
            color = HarvstDarkGreen.copy(alpha = 0.1f),
            topLeft = Offset(w * 0.1f, h * 0.2f),
            size = Size(w * 0.8f, h * 0.5f),
            cornerRadius = CornerRadius(16f, 16f)
        )
        drawRect(
            color = HarvstDarkGreen.copy(alpha = 0.1f),
            topLeft = Offset(w * 0.45f, h * 0.7f),
            size = Size(w * 0.1f, h * 0.1f)
        )
        drawRect(
            color = HarvstDarkGreen.copy(alpha = 0.1f),
            topLeft = Offset(w * 0.35f, h * 0.8f),
            size = Size(w * 0.3f, h * 0.02f)
        )

        // Phone Silhouette
        drawRoundRect(
            color = HarvstDarkGreen,
            topLeft = Offset(w * 0.6f, h * 0.4f),
            size = Size(w * 0.25f, h * 0.45f),
            cornerRadius = CornerRadius(24f, 24f)
        )
        
        // Merge Point Glow
        drawCircle(
            color = HarvstCoral.copy(alpha = 0.6f),
            radius = w * 0.1f,
            center = Offset(w * 0.65f, h * 0.5f)
        )
    }
}

@Composable
fun ControlGesturesIllustration(modifier: Modifier = Modifier) {
    Canvas(modifier = modifier.fillMaxSize()) {
        val w = size.width
        val h = size.height

        // Floating Keys
        drawRoundRect(
            color = HarvstDarkGreen,
            topLeft = Offset(w * 0.2f, h * 0.3f),
            size = Size(w * 0.15f, h * 0.15f),
            cornerRadius = CornerRadius(8f, 8f)
        )
        drawRoundRect(
            color = Color.White.copy(alpha = 0.4f),
            topLeft = Offset(w * 0.4f, h * 0.25f),
            size = Size(w * 0.15f, h * 0.15f),
            cornerRadius = CornerRadius(8f, 8f)
        )

        // Stylized Mouse
        val mousePath = Path().apply {
            moveTo(w * 0.6f, h * 0.5f)
            quadraticTo(w * 0.8f, h * 0.4f, w * 0.85f, h * 0.6f)
            quadraticTo(w * 0.9f, h * 0.8f, w * 0.7f, h * 0.85f)
            quadraticTo(w * 0.5f, h * 0.8f, w * 0.6f, h * 0.5f)
            close()
        }
        drawPath(mousePath, HarvstTan)
        
        // Cursor
        val cursorPath = Path().apply {
            moveTo(w * 0.3f, h * 0.6f)
            lineTo(w * 0.45f, h * 0.65f)
            lineTo(w * 0.4f, h * 0.7f)
            lineTo(w * 0.5f, h * 0.85f)
            lineTo(w * 0.45f, h * 0.9f)
            lineTo(w * 0.35f, h * 0.75f)
            lineTo(w * 0.3f, h * 0.85f)
            close()
        }
        drawPath(cursorPath, HarvstCoral)
    }
}

@Composable
fun DataFlowIllustration(modifier: Modifier = Modifier) {
    Canvas(modifier = modifier.fillMaxSize()) {
        val w = size.width
        val h = size.height

        // Flow lines
        repeat(3) { i ->
            val y = h * (0.4f + i * 0.1f)
            val path = Path().apply {
                moveTo(w * 0.2f, y)
                cubicTo(w * 0.4f, y - 20f, w * 0.6f, y + 20f, w * 0.8f, y)
            }
            drawPath(
                path = path,
                color = Color.White.copy(alpha = 0.3f + i * 0.2f),
                style = Stroke(width = 8f)
            )
        }

        // Floating Icons (Simplified)
        drawCircle(
            color = HarvstDarkGreen,
            radius = w * 0.05f,
            center = Offset(w * 0.3f, h * 0.35f)
        )
        drawRect(
            color = HarvstTan,
            topLeft = Offset(w * 0.6f, h * 0.55f),
            size = Size(w * 0.08f, w * 0.08f)
        )
    }
}

@Composable
fun DualScreenIllustration(modifier: Modifier = Modifier) {
    Canvas(modifier = modifier.fillMaxSize()) {
        val w = size.width
        val h = size.height

        // Main Monitor (Back)
        drawRoundRect(
            color = HarvstDarkGreen.copy(alpha = 0.05f),
            topLeft = Offset(w * 0.1f, h * 0.1f),
            size = Size(w * 0.7f, h * 0.4f),
            cornerRadius = CornerRadius(12f, 12f)
        )

        // Phone Monitor (Front)
        drawRoundRect(
            color = HarvstDarkGreen,
            topLeft = Offset(w * 0.4f, h * 0.3f),
            size = Size(w * 0.5f, h * 0.6f),
            cornerRadius = CornerRadius(20f, 20f)
        )

        // Screen Content
        drawRect(
            color = HarvstCoral.copy(alpha = 0.8f),
            topLeft = Offset(w * 0.45f, h * 0.35f),
            size = Size(w * 0.4f, h * 0.1f)
        )
        drawRect(
            color = HarvstTan.copy(alpha = 0.5f),
            topLeft = Offset(w * 0.45f, h * 0.5f),
            size = Size(w * 0.25f, h * 0.3f)
        )
    }
}
