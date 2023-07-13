//
//  AccessTokenService.swift
//  TrustId
//
//  Created by Adamos Adamou on 10/12/21.
//

import Foundation
import JWTDecode

final class AuthenticationTokenService{
    
    static let shared = AuthenticationTokenService()
    
    private init() { }
    
    public var access:String? = nil
    public var refresh:String? = nil
    
    public var userRole:UserType? {
        guard
            let access = access,
            let jwt = try? JWTDecode.decode(jwt: access),
            jwt.expired == false
        else {
            return nil
        }
        
        let role = jwt.claim(name: "role").string?.lowercased()
        switch role {
        case "student": return .student
        case "instructor": return .instructor
        default: return nil
        }
    }
    
    public var userNameSurname: (name:String, surname:String){
        guard
            let access = access,
            let jwt = try? JWTDecode.decode(jwt: access),
            jwt.expired == false
        else {
            return ("-", "-")
        }
        
        return (
            name: jwt.claim(name: "name").string ?? "-",
            surname: jwt.claim(name: "surname").string ?? "-"
        )
    }

    public var bearerToken:String {
        "Bearer \(access ?? "")"
    }
}
