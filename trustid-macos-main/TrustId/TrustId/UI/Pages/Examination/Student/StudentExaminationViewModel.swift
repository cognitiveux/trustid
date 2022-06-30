//
//  StudentExaminationViewModel.swift
//  TrustId
//
//  Created by Adamos Adamou on 28/11/21.
//

import Foundation

final class StudentExaminationViewModel:ObservableObject{
    
    // MARK: - Output
    
    @Published public var isLoading = false
    
    @Published public var exams = [StudentExam]()
    @Published public var selectedExamId:Int?
    
    @Published public var selectedExam:StudentExam = .empty
    
    // MARK: - Input
    
    public func loadExams(){
        isLoading.toggle()
        
        let request = StudentListExamApiRequest()
        request.execute { (result:Result<StudentListExamApiRequest.Response, HttpClientError>) in
            self.isLoading.toggle()
            
            switch result {
            
            case let .success(value):
                self.exams = value.resource_array
                
                if let firstExam = value.resource_array.first{
                    self.selectedExam = firstExam
                } else {
                    self.selectedExam = .empty
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
    
    public func joinExam(){
        guard selectedExam.name != "-" else {
            return
        }
        
        isLoading.toggle()
        
        let request = StudentJoinExamApiRequest(query: .init(exam_id: selectedExam.id))
        request.execute { (result:(Result<StudentJoinExamApiRequest.Response, HttpClientError>)) in
            
            self.isLoading.toggle()
            
            switch result{
            case .success(let response):
                if response.message != "Success"{
                    print("Cannot join exam")
                    return
                }
                
                self.joinExamCommand(self.selectedExam.id)
                
            case .failure(let error):
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
    
    private func joinExamCommand(_ id:String){
        NotificationCenter
            .default
            .post(name: .pageRoutingNotification, object: PageRoute.Exam(examId: id))
    }
}
