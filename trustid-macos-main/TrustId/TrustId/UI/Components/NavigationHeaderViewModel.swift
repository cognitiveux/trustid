//
//  NavigationHeaderViewModel.swift
//  TrustId
//
//  Created by Adamos Adamou on 30/11/21.
//

import Foundation

final class NavigationHeaderViewModel:ObservableObject{
    
    // Output
    
    // Input
    
    public func tappedDashboard(){
        sendPageRoutingEvent(page: .Dashboard)
    }
    
    public func tappedExaminations(){
        sendPageRoutingEvent(page: .Examination)
    }
    
//    public func tappedSettings(){
//        sendPageRoutingEvent(page: .Settings)
//    }
    
    public func tappedProfile(){
        sendPageRoutingEvent(page: .Profile)
    }
}

extension NavigationHeaderViewModel{
    
    private func sendPageRoutingEvent(page:PageRoute){
        NotificationCenter.default
            .post(name: .pageRoutingNotification, object: page)
    }
}
