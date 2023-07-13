//
//  UserFeedbackViewModel.swift
//  TrustId
//
//  Created by Adamos Adamou on 23/1/22.
//

import Foundation

final class UserFeedbackViewModel:ObservableObject{
    
    // MARK: - Initiliser
    
    private let exam_id:String
    
    init(exam_id:String){
        self.exam_id = exam_id
    }
    
    // MARK: - Output
    
    @Published public var isLoading = false
    
    @Published var checkedImpersonationBox = false{
        didSet{
            if checkedImpersonationBox == true{
                checkedApplicationBox = false
            }
        }
    }
    @Published var checkedApplicationBox = false{
        didSet{
            if checkedApplicationBox == true{
                checkedImpersonationBox = false
            }
        }
    }
    @Published var feedbackText:String = ""
    @Published var errorText:String = ""
    @Published var instructionText:String = ""
    
    // MARK: - Input
    
    public func sendFeeback(){
        if checkedImpersonationBox == false && checkedApplicationBox == false {
            errorText = "tick a check box"
            DispatchQueue.main.asyncAfter(deadline: .now() + 3) {
                self.errorText = ""
            }
            return
        }
        
        guard feedbackText.count > 0 else {
            errorText = "feedback is empty"
            DispatchQueue.main.asyncAfter(deadline: .now() + 3) {
                self.errorText = ""
            }
            return
        }
        
        isLoading.toggle()
        
        let request = StudentSubmitFeedbackApiRequest(
            query: .init(
                exam_id: exam_id,
                cheat_mode: getCheatMode(),
                feedback: feedbackText
            )
        )
        
        request.execute { (result:Result<StudentSubmitFeedbackApiRequest.Response, HttpClientError>) in
            
            self.isLoading.toggle()
            
            switch result {
            case .success(let value):
                if value.message != "Success"{
                    print("Cannot send feedback")
                    return
                }
                
                self.checkedImpersonationBox = false
                self.checkedApplicationBox = false
                self.feedbackText = ""
                
                self.instructionText = "In the next minute please try to cheat the system"
                DispatchQueue.main.asyncAfter(deadline: .now() + 60) {
                    self.instructionText = ""
                }
                
            case .failure(let error):
                print("Can't verify user")
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
    
    private func getCheatMode()->String{
        if checkedImpersonationBox{
            return "Impersonation"
        }
        
        if checkedApplicationBox{
            return "Communication"
        }
        
        return "-"
    }
}
