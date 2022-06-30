//
//  CameraStatusStore.swift
//  TrustId
//
//  Created by Adamos Adamou on 21/1/22.
//

import Foundation
import AVKit

final class CameraStatusStore:ObservableObject{
    
    @Published public var needsAuthorization = true
    
    public func checkAuthorizationStatus(){
        switch AVCaptureDevice.authorizationStatus(for: .video) {
        
        case .authorized:
            needsAuthorization = false
        
        default:
            needsAuthorization = true
            requestPermissions()
        }
    }
    
    private func requestPermissions(){
        AVCaptureDevice.requestAccess(for: .video) { granted in
            DispatchQueue.main.async{
                self.needsAuthorization = !granted
            }
        }
    }
    
    public func hasCamera() -> Bool{
        return AVCaptureDevice.default(for: .video) != nil
    }
}
