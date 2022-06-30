//
//  TrustIdApi.swift
//  TrustId
//
//  Created by Adamos Adamou on 8/12/21.
//

import Foundation

fileprivate enum Environment:String{

    case localhost = "http://localhost:10000/backend"
    case production = "https://api.trustid-project.eu/backend"
    
    public var url:URL {
        .init(string: self.rawValue)!
    }
}

enum TrustIdApi{
    private static let environment:Environment = .production
    
    public static let server:URL = environment.url
}
