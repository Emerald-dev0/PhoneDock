package com.phonedock.app.ui.onboarding

import androidx.compose.animation.*
import androidx.compose.animation.core.tween
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.pager.HorizontalPager
import androidx.compose.foundation.pager.rememberPagerState
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.phonedock.app.ui.theme.HarvstCoral
import com.phonedock.app.ui.theme.HarvstCream
import com.phonedock.app.ui.theme.HarvstDarkGreen
import com.phonedock.app.ui.theme.PhoneDockTheme
import kotlinx.coroutines.launch

data class OnboardingPage(
    val title: String,
    val description: String,
    val illustration: @Composable () -> Unit,
    val backgroundColor: Color = HarvstCream,
    val contentColor: Color = HarvstDarkGreen
)

@Composable
fun OnboardingScreen(
    onFinished: () -> Unit
) {
    val pages = listOf(
        OnboardingPage(
            title = "One\nWorkspace.",
            description = "Turn your phone into a native extension of your Windows PC. Seamlessly integrated.",
            illustration = { PhoneComputerMergeIllustration() }
        ),
        OnboardingPage(
            title = "Total\nControl.",
            description = "Use your mouse and keyboard to interact with Android applications directly from your desktop.",
            illustration = { ControlGesturesIllustration() },
            backgroundColor = HarvstCoral,
            contentColor = Color.White
        ),
        OnboardingPage(
            title = "Seamless\nSync.",
            description = "Synchronize your clipboard and transfer files with a simple drag and drop. No cloud required.",
            illustration = { DataFlowIllustration() },
            backgroundColor = HarvstCoral,
            contentColor = Color.White
        ),
        OnboardingPage(
            title = "Double\nthe View.",
            description = "Transform your Android device into a secondary high-resolution display for your PC.",
            illustration = { DualScreenIllustration() }
        )
    )

    val pagerState = rememberPagerState(pageCount = { pages.size })
    val scope = rememberCoroutineScope()

    Scaffold(
        containerColor = pages[pagerState.currentPage].backgroundColor,
        bottomBar = {
            OnboardingBottomBar(
                pageCount = pages.size,
                currentPage = pagerState.currentPage,
                contentColor = pages[pagerState.currentPage].contentColor,
                onNext = {
                    if (pagerState.currentPage < pages.size - 1) {
                        scope.launch {
                            pagerState.animateScrollToPage(pagerState.currentPage + 1)
                        }
                    } else {
                        onFinished()
                    }
                },
                onSkip = onFinished
            )
        }
    ) { padding ->
        HorizontalPager(
            state = pagerState,
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
        ) { index ->
            OnboardingPageContent(
                page = pages[index],
                modifier = Modifier.fillMaxSize()
            )
        }
    }
}

@Composable
fun OnboardingPageContent(
    page: OnboardingPage,
    modifier: Modifier = Modifier
) {
    Column(
        modifier = modifier
            .padding(horizontal = 32.dp),
        verticalArrangement = Arrangement.Center
    ) {
        Box(
            modifier = Modifier
                .weight(1f)
                .fillMaxWidth(),
            contentAlignment = Alignment.Center
        ) {
            if (page.backgroundColor == HarvstCream) {
                OrganicBlob(
                    color = HarvstCoral.copy(alpha = 0.05f),
                    modifier = Modifier.size(300.dp)
                )
            }
            
            IllustrationContainer(modifier = Modifier.size(280.dp)) {
                page.illustration()
            }
        }

        Spacer(modifier = Modifier.height(24.dp))

        EditorialHeadline(
            text = page.title,
            color = page.contentColor
        )

        Spacer(modifier = Modifier.height(16.dp))

        SupportingMessage(
            text = page.description,
            color = page.contentColor.copy(alpha = 0.7f)
        )
        
        Spacer(modifier = Modifier.height(64.dp))
    }
}

@Composable
fun OnboardingBottomBar(
    pageCount: Int,
    currentPage: Int,
    contentColor: Color,
    onNext: () -> Unit,
    onSkip: () -> Unit
) {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(32.dp)
            .navigationBarsPadding()
    ) {
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            StepIndicator(
                pageCount = pageCount,
                currentPage = currentPage,
                activeColor = if (contentColor == Color.White) Color.White else HarvstCoral,
                inactiveColor = contentColor.copy(alpha = 0.2f)
            )

            TextButton(onClick = onSkip) {
                Text(
                    "Skip",
                    color = contentColor.copy(alpha = 0.5f),
                    style = MaterialTheme.typography.labelLarge
                )
            }
        }

        Spacer(modifier = Modifier.height(24.dp))

        PremiumButton(
            text = if (currentPage == pageCount - 1) "GET STARTED" else "NEXT",
            onClick = onNext,
            containerColor = HarvstDarkGreen,
            contentColor = Color.White
        )
    }
}
