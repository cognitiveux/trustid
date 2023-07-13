//
//  StudentIdentificationStep1ApiRequest.swift
//  TrustId
//
//  Created by Adamos Adamou on 10/12/21.
//

import Foundation

struct StudentIdentificationStep1ApiRequest: ApiRequest{
    typealias B = Query
    typealias R = Response
    
    struct Query:Encodable {
        let image:String
    }
    
    struct Response:Decodable {
        let message:String
        let resource_name:String
        let resource_str:String
    }
    
    let path: URL = TrustIdApi.server.appendingPathComponent("student/identification")
    let method: HttpMethod = .post
    let headers:[HttpHeader] = [
        .init(name:"Authorization", value: AuthenticationTokenService.shared.bearerToken)
    ]
    let body: Query?

    init(query:Query){
        self.body = query
    }
}
