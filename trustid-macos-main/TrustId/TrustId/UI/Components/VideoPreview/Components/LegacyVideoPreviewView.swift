//
//  LegacyVideoPreviewView.swift
//  TrustId
//
//  Created by Adamos Adamou on 14/12/21.
//

import Foundation
import AppKit
import AVFoundation

final class LegacyVideoPreviewView: NSView{
    
    public func startPreview(with session:AVCaptureSession){
        self.layer = makeAVCaptureVideoPreviewLayer(session: session)
    }
    
    private func makeAVCaptureVideoPreviewLayer(session:AVCaptureSession) -> AVCaptureVideoPreviewLayer{
        let layer = AVCaptureVideoPreviewLayer(session: session)
        mirrorPreview(layer: layer)
        return layer
    }
    
    private func mirrorPreview(layer:AVCaptureVideoPreviewLayer){
        guard let connection = layer.connection, connection.isVideoMirroringSupported  else { return }
        connection.automaticallyAdjustsVideoMirroring = false
        connection.isVideoMirrored = true
    }
}
