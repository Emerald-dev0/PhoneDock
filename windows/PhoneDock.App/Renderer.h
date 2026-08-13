#pragma once

#include <windows.h>
#include <d3d11_1.h>
#include <dxgi1_3.h>
#include <wrl/client.h>
#include <winrt/base.h>

namespace PhoneDock::App {

class Renderer {
public:
    Renderer();
    ~Renderer();

    bool Initialize(uint32_t width, uint32_t height);
    void Present(ID3D11Texture2D* texture);

    ID3D11Device* GetDevice() { return m_d3dDevice.Get(); }
    ID3D11DeviceContext* GetContext() { return m_d3dContext.Get(); }

private:
    Microsoft::WRL::ComPtr<ID3D11Device> m_d3dDevice;
    Microsoft::WRL::ComPtr<ID3D11DeviceContext> m_d3dContext;
    Microsoft::WRL::ComPtr<IDXGISwapChain1> m_swapChain;

    // Video Processor for NV12 -> BGRA
    Microsoft::WRL::ComPtr<ID3D11VideoDevice> m_videoDevice;
    Microsoft::WRL::ComPtr<ID3D11VideoContext> m_videoContext;
    Microsoft::WRL::ComPtr<ID3D11VideoProcessor> m_videoProcessor;
    Microsoft::WRL::ComPtr<ID3D11VideoProcessorEnumerator> m_videoProcessorEnum;
};

} // namespace PhoneDock::App
