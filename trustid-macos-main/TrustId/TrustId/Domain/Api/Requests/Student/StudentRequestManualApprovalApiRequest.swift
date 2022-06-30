//
//  StudentRequestManualApprovalApiRequest.swift
//  TrustId
//
//  Created by Adamos Adamou on 24/1/22.
//

import Foundation

struct StudentRequestManualApprovalApiRequest: ApiRequest{
    typealias B = Query
    typealias R = Response
    
    struct Query:Encodable {
        let exam_id:String
    }
    
    struct Response:Decodable {
        let message:String
        let resource_name:String
    }
    
    let path: URL = TrustIdApi.server.appendingPathComponent("student/request_manual_approval")
    let method: HttpMethod = .post
    let headers:[HttpHeader] = [
        .init(name:"Authorization", value: AuthenticationTokenService.shared.bearerToken),
    ]
    let body: Query?

    init(query:Query){
        self.body = query
    }
}
