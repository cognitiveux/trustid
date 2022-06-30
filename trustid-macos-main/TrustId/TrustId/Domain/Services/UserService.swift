//
//  UserService.swift
//  TrustId
//
//  Created by Adamos Adamou on 25/11/21.
//

import Foundation

final class UserService{
    
    static let shared = UserService()
    
    private init() { }
    
    private var currentUser:User?
    
    public func store(user:User){
        self.currentUser = user
    }
    
    public func retrieveUser() -> User? {
        return currentUser
    }
}
