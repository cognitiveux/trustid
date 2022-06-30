//
//  StudentListExam.swift
//  TrustId
//
//  Created by Adamos Adamou on 9/12/21.
//

import Foundation

struct StudentListExamApiRequest: ApiRequest{
    typealias B = Query
    typealias R = Response
    
    struct Query:Encodable { }
    
    struct Response:Decodable {
        let message:String
        let resource_name:String
        let resource_array:[StudentExam]
    }
    
    let path: URL = TrustIdApi.server.appendingPathComponent("student/list_exam")
    let method: HttpMethod = .get
    let body: Query?
    let headers:[HttpHeader] = [
        .init(name:"Authorization", value: AuthenticationTokenService.shared.bearerToken),
    ]
    
    init(){
        body = nil
    }
}

extension StudentExam: Decodable{
    
    enum CodingKeys: String, CodingKey {
        case id = "exam_id"
        case name
        case status
        case scheduled = "scheduled_date"
        case privacyPolicy = "privacy_policy"
        case additionalMaterial = "additional_material"
        case duration
        case examType = "exam_type"
    }
    
    init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)
        
        let examIdInt = try container.decode(Int.self, forKey: .id)
        self.id = examIdInt.description
        self.name = try container.decode(String.self, forKey: .name)
        self.status = try container.decode(String.self, forKey: .status)
        let dateString = try container.decode(String.self, forKey: .scheduled)
        self.scheduled = StudentExam.mapDateUTC(dateString: dateString)!
        self.privacyPolicy = try container.decode(String.self, forKey: .privacyPolicy)
        self.additionalMaterial = try container.decode(Bool.self, forKey: .additionalMaterial)
        self.duration = try container.decode(Int.self, forKey: .duration)
        self.examType = try container.decode(String.self, forKey: .examType)
    }
    
    private static func mapDateUTC(dateString:String) -> Date?{
        let dateFormatter = DateFormatter()
        dateFormatter.dateFormat = "yyyy-MM-dd'T'HH:mm:ss"
        dateFormatter.timeZone = TimeZone(abbreviation: "UTC")
        return dateFormatter.date(from: dateString)
    }
}
