//
//  InstructorUpdateExamDetailsApiRequest.swift
//  TrustId
//
//  Created by Adamos Adamou on 10/12/21.
//

import Foundation

struct InstructorUpdateExamDetailsApiRequest: ApiRequest{
    
    typealias B = Query
    typealias R = Response
    
    struct Query:Encodable {
        let exam_id:String
        let privacy_policy:String
        let duration:Int
        let exam_type:String
        let additional_material:Bool
        let scheduledDate:String
    }
    
    struct Response:Decodable {
        let message:String
        let resource_name:String
    }
    
    let path: URL = TrustIdApi.server.appendingPathComponent("instructor/update_exam_condition")
    let method: HttpMethod = .post
    let headers:[HttpHeader] = [
        .init(name:"Authorization", value: AuthenticationTokenService.shared.bearerToken)
    ]
    let body: Query?
    
    init(body: Query) {
        self.body = body
    }
}
