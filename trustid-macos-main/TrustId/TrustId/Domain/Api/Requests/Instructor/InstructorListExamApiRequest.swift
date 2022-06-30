//
//  InstructorListExamApiRequest.swift
//  TrustId
//
//  Created by Adamos Adamou on 10/12/21.
//

import Foundation

struct InstructorListExamApiRequest: ApiRequest{
    typealias B = Query
    typealias R = Response
    
    struct Query:Encodable { }
    
    struct Response:Decodable {
        let message:String
        let resource_name:String
        let resource_array:[InstructorExam]
    }
    
    let path: URL = TrustIdApi.server.appendingPathComponent("instructor/list_exam")
    let method: HttpMethod = .get
    let headers:[HttpHeader] = [
        .init(name:"Authorization", value: AuthenticationTokenService.shared.bearerToken),
    ]
    let body: Query?
    
    init(){
        body = nil
    }
}

extension InstructorExam: Decodable{
    
    enum CodingKeys: String, CodingKey {
        case id = "exam_id"
        case name
        case status
        case scheduled = "scheduled_date"
        case privacyPolicy = "privacy_policy"
        case additionalMaterial = "additional_material"
        case duration
        case examType = "exam_type"
        case enrolledStudents = "enrolled_students"
    }
    
    init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)
        
        let examIdInt = try container.decode(Int.self, forKey: .id)
        self.id = examIdInt.description
        self.name = try container.decode(String.self, forKey: .name)
        self.status = try container.decode(String.self, forKey: .status)
        let dateString = try container.decode(String.self, forKey: .scheduled)
        self.scheduled = InstructorExam.mapDateUTC(dateString: dateString)!
        self.privacyPolicy = try container.decode(String.self, forKey: .privacyPolicy)
        self.additionalMaterial = try container.decode(Bool.self, forKey: .additionalMaterial)
        self.duration = try container.decode(Int.self, forKey: .duration)
        self.examType = try container.decode(String.self, forKey: .examType)
        self.enrolledStudents = try container.decode([EnrolledStudent].self, forKey: .enrolledStudents)
    }
    
    private static func mapDateUTC(dateString:String) -> Date?{
        let dateFormatter = DateFormatter()
        dateFormatter.dateFormat = "yyyy-MM-dd'T'HH:mm:ss"
        dateFormatter.timeZone = TimeZone(abbreviation: "UTC")
        return dateFormatter.date(from: dateString)
    }
}

extension EnrolledStudent: Decodable{
    enum CodingKeys: String, CodingKey {
        case email
        case name
        case verificationStatus = "verification_status"
    }
    
    init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)
        
        self.email = try container.decode(String.self, forKey: .email)
        self.name = try container.decode(String.self, forKey: .name)
        self.verificationStatus = try container.decode(String.self, forKey: .verificationStatus)
    }
}
