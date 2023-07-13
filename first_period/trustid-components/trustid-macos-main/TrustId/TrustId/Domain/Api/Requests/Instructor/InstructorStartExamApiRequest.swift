//
//  InstructorStartExamApiRequest.swift
//  TrustId
//
//  Created by Adamos Adamou on 10/12/21.
//

import Foundation

struct InstructorStartExamApiRequest: ApiRequest{
    
    typealias B = Query
    typealias R = Response
    
    struct Query:Encodable {
        let condition:String = "Start"
        let exam_id:String
    }
    
    struct Response:Decodable {
        let message:String
        let resource_name:String
    }
    
    let path: URL = TrustIdApi.server.appendingPathComponent("update_exam_condition")
    let method: HttpMethod = .post
    let headers:[HttpHeader] = [
        .init(name:"Authorization", value: AuthenticationTokenService.shared.bearerToken)
    ]
    let body: Query?
    
    init(body: Query) {
        self.body = body
    }
}
