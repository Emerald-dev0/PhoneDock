package com.phonedock.app.ui.onboarding

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.phonedock.app.ui.theme.HarvstCoral
import com.phonedock.app.ui.theme.HarvstCream
import com.phonedock.app.ui.theme.HarvstDarkGreen

@Composable
fun EditorialHeadline(
    text: String,
    modifier: Modifier = Modifier,
    color: Color = HarvstDarkGreen,
    textAlign: TextAlign = TextAlign.Start
) {
    Text(
        text = text,
        modifier = modifier,
        style = MaterialTheme.typography.displayMedium.copy(
            fontWeight = FontWeight.Black,
            lineHeight = 44.sp,
            letterSpacing = (-1).sp
        ),
        color = color,
        textAlign = textAlign
    )
}

@Composable
fun SupportingMessage(
    text: String,
    modifier: Modifier = Modifier,
    color: Color = HarvstDarkGreen.copy(alpha = 0.7f)
) {
    Text(
        text = text,
        modifier = modifier,
        style = MaterialTheme.typography.bodyLarge.copy(
            lineHeight = 24.sp,
            letterSpacing = 0.2.sp
        ),
        color = color
    )
}

@Composable
fun PremiumButton(
    text: String,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    containerColor: Color = HarvstDarkGreen,
    contentColor: Color = Color.White
) {
    Button(
        onClick = onClick,
        modifier = modifier
            .height(64.dp)
            .fillMaxWidth(),
        shape = RoundedCornerShape(16.dp),
        colors = ButtonDefaults.buttonColors(
            containerColor = containerColor,
            contentColor = contentColor
        ),
        elevation = ButtonDefaults.buttonElevation(defaultElevation = 0.dp)
    ) {
        Text(
            text = text,
            style = MaterialTheme.typography.titleMedium.copy(
                fontWeight = FontWeight.Bold,
                letterSpacing = 1.sp
            )
        )
    }
}

@Composable
fun StepIndicator(
    pageCount: Int,
    currentPage: Int,
    modifier: Modifier = Modifier,
    activeColor: Color = HarvstCoral,
    inactiveColor: Color = HarvstDarkGreen.copy(alpha = 0.1f)
) {
    Row(
        modifier = modifier,
        horizontalArrangement = Arrangement.spacedBy(8.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        repeat(pageCount) { index ->
            val isSelected = index == currentPage
            Box(
                modifier = Modifier
                    .height(4.dp)
                    .width(if (isSelected) 24.dp else 12.dp)
                    .clip(CircleShape)
                    .background(if (isSelected) activeColor else inactiveColor)
            )
        }
    }
}

@Composable
fun OrganicBlob(
    color: Color,
    modifier: Modifier = Modifier
) {
    Canvas(modifier = modifier) {
        val path = Path().apply {
            moveTo(size.width * 0.2f, size.height * 0.1f)
            quadraticTo(size.width * 0.5f, 0f, size.width * 0.8f, size.height * 0.2f)
            quadraticTo(size.width, size.height * 0.5f, size.width * 0.7f, size.height * 0.8f)
            quadraticTo(size.width * 0.4f, size.height, size.width * 0.1f, size.height * 0.7f)
            quadraticTo(0f, size.height * 0.4f, size.width * 0.2f, size.height * 0.1f)
            close()
        }
        drawPath(path, color)
    }
}
