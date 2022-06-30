//
//  StudentIdentificationStep3ApiRequest.swift
//  TrustId
//
//  Created by Adamos Adamou on 10/12/21.
//

import Foundation

struct StudentIdentificationStep3ApiRequest: ApiRequest{
    typealias B = Query
    typealias R = Response
    
    struct Query:Encodable {
        let running_processes:[String]
    }
    
    struct Response:Decodable {
        let message:String
        let resource_name:String
        let resource_array:[String]
    }
    
    let path: URL = TrustIdApi.server.appendingPathComponent("student/checkup_process")
    let method: HttpMethod = .post
    let headers:[HttpHeader] = [
        .init(name:"Authorization", value: AuthenticationTokenService.shared.bearerToken),
    ]
    let body: Query?

    init(query:Query){
        self.body = query
    }
}
