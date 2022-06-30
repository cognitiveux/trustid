//
//  ProfilePageViewModel.swift
//  TrustId
//
//  Created by Adamos Adamou on 16/1/22.
//

import Foundation

final class ProfilePageViewModel:ObservableObject{
    
    // MARK: Dependencies
    
    private var tokenService = AuthenticationTokenService.shared
    private var userService = UserService.shared
    
    init(){
        user = userService.retrieveUser() ?? .init(name: "-", surname: "-", type: .student)
    }
    
    // MARK: - Output
    
    @Published public var isLoading = false
    
    @Published public var user:User
    
    // MARK: - Input
    
    public func logout(){
        AuthenticationTokenService.shared.access = nil
        AuthenticationTokenService.shared.refresh = nil
        
        NotificationCenter.default
            .post(name: .userAuthenticatedNotification, object: nil)
    }
}
