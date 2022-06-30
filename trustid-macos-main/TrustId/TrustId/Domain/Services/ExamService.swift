//
//  ExamService.swift
//  TrustId
//
//  Created by Adamos Adamou on 3/1/22.
//

import Foundation

struct ExamService{
    

    // Dependencies
    
    private let userService = UserService.shared
    
    // Public Methods
    
    public typealias responseHandler = (Result<[Exam], HttpClientError>) -> Void
    
    public func execute(completion: @escaping responseHandler){
        guard let user = userService.retrieveUser() else {
            print("Cant find user")
            return
        }
        
        switch user.type{
        case .student: loadStudentExams(completion: completion)
        case .instructor: loadInstructorExams(completion: completion)
        }
    }
        
    // Private Methods
    
    private func loadStudentExams(completion: @escaping responseHandler){
        let request = StudentListExamApiRequest()
        request.execute { (result:Result<StudentListExamApiRequest.Response, HttpClientError>) in
            switch result {
            case let .success(value): completion(.success(map(value.resource_array)))
            case let .failure(error): completion(.failure(error))
            }
        }
    }
    
    private func loadInstructorExams(completion: @escaping responseHandler){
        let request = InstructorListExamApiRequest()
        request.execute { (result:Result<InstructorListExamApiRequest.Response, HttpClientError>) in
            switch result {
            case let .success(value): completion(.success(map(value.resource_array)))
            case let .failure(error): completion(.failure(error))
            }
        }
    }
    
    // Mappers
    
    private func map(_ exam:StudentExam) -> Exam{
        .init(id: exam.id, name: exam.name, status: exam.status, scheduled: exam.scheduled)
    }

    private func map(_ exams:[StudentExam]) -> [Exam]{
        exams.map{map($0)}
    }

    private func map(_ exam:InstructorExam) -> Exam{
        .init(id: exam.id, name: exam.name, status: exam.status, scheduled: exam.scheduled)
    }

    private func map(_ exams:[InstructorExam]) -> [Exam]{
        exams.map{map($0)}
    }
}
