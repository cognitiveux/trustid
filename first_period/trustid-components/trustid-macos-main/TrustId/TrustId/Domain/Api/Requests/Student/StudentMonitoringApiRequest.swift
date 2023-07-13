//
//  StudentMonitoringApiRequest.swift
//  TrustId
//
//  Created by Adamos Adamou on 10/12/21.
//

import Foundation

struct StudentMonitoringApiRequest: ApiRequest{
    typealias B = Query
    typealias R = Response
    
    struct Query:Encodable {
        let exam_id:String
        let running_processes:[String]
        let ip_address:String
        let image:String
    }
    
    struct Response:Decodable {
        let message:String
        let resource_name:String
    }
    
    let path: URL = TrustIdApi.server.appendingPathComponent("student/monitoring")
    let method: HttpMethod = .post
    let headers:[HttpHeader] = [
        .init(name:"Authorization", value: AuthenticationTokenService.shared.bearerToken)
    ]
    let body: Query?

    init(query:Query){
        self.body = query
    }
}
