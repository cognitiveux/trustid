//
//  VideoPreviewView.swift
//  TrustId
//
//  Created by Adamos Adamou on 14/12/21.
//

import Foundation
import AVFoundation
import SwiftUI

struct VideoPreviewView: NSViewRepresentable {

    // UI
    
    private var videoPreviewView = LegacyVideoPreviewView()
    
    // Dependencies
    
    private let session: AVCaptureSession
    private let startSessionCallback: ()->Void
    
    public init(session: AVCaptureSession, startSessionCallback: @escaping () -> Void) {
        self.session = session
        self.startSessionCallback = startSessionCallback
    }
    
    func makeNSView(context: Context) -> NSView {
        startSessionCallback()

        videoPreviewView.startPreview(with: session)
        
        return videoPreviewView
    }
    
    func updateNSView(_ uiView: NSView, context: Context) { }
}
