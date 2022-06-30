//
//  VideoPreviewViewModel.swift
//  TrustId
//
//  Created by Adamos Adamou on 14/12/21.
//

import Foundation
import AVFoundation
import AppKit

final class VideoPreviewViewModel:NSObject, ObservableObject{
    
    @Published public var session = AVCaptureSession()
    
    @Published public var isRunning = false
    
    private var photoCaptureWrapper:WrappedDelegate?
    
    // Dependencies
    
    private var photoOutput = AVCapturePhotoOutput()
    
    // Methods
    
    override init() {
        super.init()
        setupConfiguration()
    }
    
    public func toggleSession(){
        isRunning ? stopSession() : startSession()
    }
    
    public func capturePhoto(completion:@escaping (NSImage)->Void){
        photoCaptureWrapper = WrappedDelegate(didCapturedImageHandler: completion)
        
        let settings = AVCapturePhotoSettings()
        photoOutput.capturePhoto(with: settings, delegate: photoCaptureWrapper!)
    }
    
    // MARK: Private
    
    private func setupConfiguration(){
        session.beginConfiguration()
        if let frontCameraDevice = AVCaptureDevice.default(.builtInWideAngleCamera,for: .video, position: .front) {
            do {
                if let device = try? AVCaptureDeviceInput(device: frontCameraDevice){
                    session.addInput(device)
                    
                    photoOutput = AVCapturePhotoOutput()
                    session.addOutput(photoOutput)
                } else {
                    print("Error: Camera configuration cant create device input")
                }
            }
        }
        session.commitConfiguration()
    }
    
    private func startSession(){
        session.startRunning()
        isRunning = true
    }
    
    private func stopSession(){
        session.stopRunning()
        isRunning = false
    }
}

fileprivate final class WrappedDelegate:NSObject, AVCapturePhotoCaptureDelegate{
    
    private var didCapturedImage:(NSImage)->Void
    
    init(didCapturedImageHandler:@escaping (NSImage)->Void){
        self.didCapturedImage = didCapturedImageHandler
    }
    
    func photoOutput(_ output: AVCapturePhotoOutput, didFinishProcessingPhoto photo: AVCapturePhoto, error: Error?) {
        guard
            let data = photo.fileDataRepresentation(),
            let image = NSImage(data: data)
        else {
            return
        }
        
//        didCapturedImage(image.flipped(flipHorizontally: true))
        didCapturedImage(image.flipped(flipHorizontally: true).scaledCopy(sizeOfLargerSide: 480))
    }
}

// MARK: - Utilities

extension NSImage {
    func flipped(flipHorizontally: Bool = false, flipVertically: Bool = false) -> NSImage {
        let flippedImage = NSImage(size: size)

        flippedImage.lockFocus()

        NSGraphicsContext.current?.imageInterpolation = .high

        let transform = NSAffineTransform()
        transform.translateX(by: flipHorizontally ? size.width : 0, yBy: flipVertically ? size.height : 0)
        transform.scaleX(by: flipHorizontally ? -1 : 1, yBy: flipVertically ? -1 : 1)
        transform.concat()

        draw(at: .zero, from: NSRect(origin: .zero, size: size), operation: .sourceOver, fraction: 1)

        flippedImage.unlockFocus()

        return flippedImage
    }
    
    func scaledCopy(sizeOfLargerSide: CGFloat) -> NSImage {
        var newW: CGFloat
        var newH: CGFloat
        var scaleFactor: CGFloat
        
        if self.size.width > self.size.height {
            scaleFactor = self.size.width / sizeOfLargerSide
            newW = sizeOfLargerSide
            newH = self.size.height / scaleFactor
        } else {
            scaleFactor = self.size.height / sizeOfLargerSide
            newH = sizeOfLargerSide
            newW = self.size.width / scaleFactor
        }
        
        return resizedCopy(w: newW, h: newH)
    }
    
    func resizedCopy(w: CGFloat, h: CGFloat) -> NSImage {
        let destSize = NSMakeSize(w, h)
        let newImage = NSImage(size: destSize)
        
        newImage.lockFocus()
        
        self.draw(
            in: NSRect(origin: .zero, size: destSize),
            from: NSRect(origin: .zero, size: self.size),
            operation: .copy,
            fraction: CGFloat(1)
        )
        
        newImage.unlockFocus()
        
        guard
            let data = newImage.tiffRepresentation,
            let result = NSImage(data: data)
        else { return NSImage() }
        
        return result
    }
}
