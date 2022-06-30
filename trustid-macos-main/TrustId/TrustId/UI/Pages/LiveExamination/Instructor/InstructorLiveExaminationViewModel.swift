//
//  InstructorLiveExaminationViewModel.swift
//  TrustId
//
//  Created by Adamos Adamou on 23/1/22.
//

import Foundation

final class InstructorLiveExaminationViewModel:ObservableObject{
    
    // MARK: - Initiliser
    
    private let exam_id:String
    
    init(exam_id:String){
        self.exam_id = exam_id
    }
    
    // MARK: - Output
    
    @Published public var isLoading = false
    
    @Published public var enrolledStudents = [InstructorLiveExaminationView.EnrolledStudent]()
    @Published public var alerts = [AlertListView.Alert]()
    
    // MARK: - Input
    
    public func loadEnrolledStudents(){
        isLoading.toggle()
        
        let request = InstructorListExamApiRequest()
        request.execute { (result:Result<InstructorListExamApiRequest.Response, HttpClientError>) in
            self.isLoading.toggle()
            
            switch result {
            
            case let .success(value):
                
                guard let selectedExam = value.resource_array.first(where: {$0.id == self.exam_id}) else {
                    return
                }
                
                self.enrolledStudents = selectedExam.enrolledStudents.map{ student in
                    let splits = student.name.split(separator: " ")
                    if splits.count > 1{
                        return .init(email: student.email, name: splits[0].description, surname: splits[1].description, status: student.verificationStatus)
                    }
                    return .init(email: student.email, name: student.name, surname: "-", status: student.verificationStatus)
                }
              
            case let .failure(error):
                print(error.localizedDescription)
                switch error{
                case .failed(_):
                    print("ApiError: -failed")
                case .noData:
                    print("ApiError: -noData")
                case .apiErrorResponse(let statusCode, let data):
                    print("ApiError: \(statusCode) \(data.message)")
                }
            }
        }
    }
    
    public func closeExam(){
        
        // temporary fix until api request is ready
        self.closeExamCommand()
        
//        isLoading.toggle()
//
//        let request = InstructorCloseExamApiRequest(body: .init(exam_id: exam_id))
//        request.execute { (result:(Result<InstructorCloseExamApiRequest.Response, HttpClientError>)) in
//
//            self.isLoading.toggle()
//
//            switch result{
//            case .success(let response):
//                if response.message != "Success"{
//                    print("Cannot close exam")
//                    return
//                }
//
//                self.closeExamCommand()
//
//            case .failure(let error):
//                print(error.localizedDescription)
//                switch error{
//                case .failed(_):
//                    print("ApiError: -failed")
//                case .noData:
//                    print("ApiError: -noData")
//                case .apiErrorResponse(let statusCode, let data):
//                    print("ApiError: \(statusCode) \(data.message)")
//                }
//            }
//        }
    }
    
    public func approvedStudent(student:InstructorLiveExaminationView.EnrolledStudent){
        isLoading.toggle()
        
        let request = InstructorManualApproveStudentApiRequest(body: .init(email: student.email, exam_id: self.exam_id))
        request.execute { (result:Result<InstructorListExamApiRequest.Response, HttpClientError>) in
            self.isLoading.toggle()
            
            switch result {
            
            case .success(_):
                self.loadEnrolledStudents()
              
            case let .failure(error):
                print(error.localizedDescription)
                switch error{
                case .failed(_):
                    print("ApiError: -failed")
                case .noData:
                    print("ApiError: -noData")
                case .apiErrorResponse(let statusCode, let data):
                    print("ApiError: \(statusCode) \(data.message)")
                }
            }
        }
    }
    
    // MARK: Internal
    
    private func closeExamCommand(){
        NotificationCenter
            .default
            .post(name: .pageRoutingNotification, object: PageRoute.Examination)
    }
}
