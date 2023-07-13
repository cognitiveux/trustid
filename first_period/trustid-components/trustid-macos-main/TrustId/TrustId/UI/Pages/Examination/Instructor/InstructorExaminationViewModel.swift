//
//  InstructorExaminationViewModel.swift
//  TrustId
//
//  Created by Adamos Adamou on 29/11/21.
//

import Foundation

final class InstructorExaminationViewModel:ObservableObject{
    
    // MARK: - Output
    
    @Published public var isLoading = false
    
    @Published public var exams = [InstructorExam]()
    @Published public var selectedExamId:Int?
    
    @Published public var selectedExam:InstructorExam = .empty
    
    // MARK: - Input
    
    public func loadExams(){
        isLoading.toggle()
        
        let request = InstructorListExamApiRequest()
        request.execute { (result:Result<InstructorListExamApiRequest.Response, HttpClientError>) in
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
    
    public func startExam(){
        guard selectedExam.name != "-" else {
            return
        }
        
        isLoading.toggle()
        
        let request = InstructorStartExamApiRequest(body: .init(exam_id: selectedExam.id))
        request.execute { (result:(Result<InstructorStartExamApiRequest.Response, HttpClientError>)) in
            
            self.isLoading.toggle()
            
            switch result{
            case .success(let response):
                if response.message != "Success"{
                    print("Cannot start exam")
                    return
                }
                
                self.startExamCommand(self.selectedExam.id)
                
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

    private func startExamCommand(_ id:String){
        NotificationCenter
            .default
            .post(name: .pageRoutingNotification, object: PageRoute.Exam(examId: id))
    }
}
