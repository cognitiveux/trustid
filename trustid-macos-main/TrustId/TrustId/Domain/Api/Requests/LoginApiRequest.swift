//
//  LoginApiRequest.swift
//  TrustId
//
//  Created by Adamos Adamou on 8/12/21.
//

import Foundation

struct LoginApiRequest: ApiRequest{
    typealias B = Query
    typealias R = Response
    
    struct Query:Encodable {
        let email:String
        let password:String
    }
    
    struct Response:Decodable {
        let message:String
        let resource_name:String
        let resource_obj:LoginResponseObject
    }
    
    let path: URL = TrustIdApi.server.appendingPathComponent("login")
    let method: HttpMethod = .post
    let headers: [HttpHeader] = []
    let body: Query?
    
    init(query:Query){
        body = query
    }
}

struct LoginResponseObject:Decodable{
    let access:String
    let refresh:String
}
