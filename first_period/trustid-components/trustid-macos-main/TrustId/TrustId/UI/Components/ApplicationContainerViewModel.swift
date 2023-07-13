//
//  ApplicationContainerViewModel.swift
//  TrustId
//
//  Created by Adamos Adamou on 22/11/21.
//

import Foundation
import Combine

final class ApplicationContainerViewModel:ObservableObject{
    
    @Published public var isLoggedIn = false
    @Published public var route:PageRoute = .Dashboard
    
    private let authenticationEventsPublisher = NotificationCenter
        .default
        .publisher(for: .userAuthenticatedNotification)
    
    private let routingEventsPublisher = NotificationCenter
        .default
        .publisher(for: .pageRoutingNotification)
    
    private var cancellables = Set<AnyCancellable>()
    
    init(){
        authenticationEventsPublisher
            .sink { [weak self] value in
                self?.checkUserAuthenticationStatus()
            }
            .store(in: &cancellables)
        
        routingEventsPublisher
            .sink { [weak self] notification in
                if let object = notification.object {
                    self?.processRoutingNotification(object)
                }
            }
            .store(in: &cancellables)
    }
    
    private func checkUserAuthenticationStatus(){
        
        guard
            let _ = UserService.shared.retrieveUser(),
            let _ = AuthenticationTokenService.shared.userRole
        else {
            route = .Dashboard
            isLoggedIn = false
            return
        }

        isLoggedIn = true
    }
    
    private func processRoutingNotification(_ object:Any){
        guard let pageRoute = object as? PageRoute else { return }
        
        route = pageRoute
    }
}
