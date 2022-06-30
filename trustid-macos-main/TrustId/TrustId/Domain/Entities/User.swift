//
//  User.swift
//  TrustId
//
//  Created by Adamos Adamou on 23/11/21.
//

import Foundation

struct User{
    let name:String
    let surname:String
    let type:UserType
}

extension User{
    var initials:String{
        guard
            let nameFirstLetter = name.first,
            let surnameFirstLetter = surname.first
        else {
            return "-"
        }
        
        return "\(nameFirstLetter.uppercased())\(surnameFirstLetter.uppercased())"
    }
    
    var fullName:String{
        return "\(name) \(surname)"
    }
}
