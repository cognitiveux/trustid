//
//  InstructorManualApproveStudentApiRequest.swift
//  TrustId
//
//  Created by Adamos Adamou on 24/1/22.
//

import Foundation

struct InstructorManualApproveStudentApiRequest: ApiRequest{
    
    typealias B = Query
    typealias R = Response
    
    struct Query:Encodable {
        let email:String
        let exam_id:String
    }
    
    struct Response:Decodable {
        let message:String
        let resource_name:String
    }
    
    let path: URL = TrustIdApi.server.appendingPathComponent("instructor/manual_approve_student")
    let method: HttpMethod = .post
    let headers:[HttpHeader] = [
        .init(name:"Authorization", value: AuthenticationTokenService.shared.bearerToken)
    ]
    let body: Query?
    
    init(body: Query) {
        self.body = body
    }
}
