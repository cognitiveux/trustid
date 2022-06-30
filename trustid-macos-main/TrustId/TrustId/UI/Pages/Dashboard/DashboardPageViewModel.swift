//
//  DashboardPageViewModel.swift
//  TrustId
//
//  Created by Adamos Adamou on 30/11/21.
//

import Foundation

final class DashboardPageViewModel:ObservableObject{
    
    // Output
    
    @Published public var showErrorDialog = false
    @Published public var showErrorDialogMessage = "-"
    
    @Published public var isLoading = false
    
    @Published public var exams = [Exam]()
    
    public var defaultExam:Exam = .empty
    
    // Input
    
    public func tappedJoinExam(){
        
        guard let liveExam = exams.first(where: {$0.isStarted}) else {
            return
        }
        
        sendPageRoutingEvent(page: .Exam(examId: liveExam.id))
    }
    
    public func tappedViewExams(){
        sendPageRoutingEvent(page: .Examination)
    }
    
    public func loadExams(){
        isLoading.toggle()
        
        let service = ExamService()
        service.execute { (result: Result<[Exam], HttpClientError>) in
            self.isLoading.toggle()
            
            switch result {
            case .success(let exams):
                self.exams = exams
                
            case .failure(let error):
                print(error.localizedDescription)
                switch error{
                case .failed(_):
                    print("ApiError: -failed")
                case .noData:
                    print("ApiError: -noData")
                case .apiErrorResponse(let statusCode, let data):
                    print("ApiError: \(statusCode) \(data.message)")
                    self.showErrorDialogMessage = data.message
                    self.showErrorDialog.toggle()
                }
            }
        }
    }
}

extension DashboardPageViewModel{
    
    private func sendPageRoutingEvent(page:PageRoute){
        NotificationCenter.default
            .post(name: .pageRoutingNotification, object: page)
    }
}

