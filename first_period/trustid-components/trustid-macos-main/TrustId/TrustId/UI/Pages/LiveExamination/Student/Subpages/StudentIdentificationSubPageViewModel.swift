//
//  StudentIdentificationSubPageViewModel.swift
//  TrustId
//
//  Created by Adamos Adamou on 28/12/21.
//

import Foundation
import SwiftUI

extension NSImage {
    var base64String: String? {

        guard
            let data = self.tiffRepresentation,
            let bitmap = NSBitmapImageRep(data: data)
        else {
            print("Couldn't create bitmap representation")
            return nil
        }
        
        let properties = [NSBitmapImageRep.PropertyKey.compressionFactor: 1.0]
        
        guard let pngData = bitmap.representation(using: .png, properties: properties) else {
            print("Couldn't create PNG")
            return nil
        }
        
        return pngData.base64EncodedString()
    }
}

final class StudentIdentificationSubPageViewModel:ObservableObject{
    
    // MARK: - Initiliser
    
    private let exam_id:String
    
    init(exam_id:String){
        self.exam_id = exam_id
    }
    
    enum IdentificationStep{
        case getStarted, face, confirmIdentity, runningApplications, identified
    }
    
    enum ButtonState{
        case visible, hidden, disabled
    }
    
    // MARK: - Output
    
    @Published public var isLoading = false
    @Published var currentStep:IdentificationStep = .getStarted
    @Published var showIdentityConfirmationDialog = false
    @Published var showIdentificationFailureDialog = false
    @Published var identifiedUser = ""
    @Published var showRequestInstructorApprovalButton = ButtonState.hidden
    @Published var showInstructorIdentityConfirmationDialog = false
    
    @Published var runningApplicationsNeedsCheck = true
    @Published var blockingApplications = [String]()

    // MARK: - Input
    
    public func executeStep(){
        switch currentStep {
        case .getStarted: executeGetStartedStep()
        case .face: executeFaceIdentificationStep()
        case .confirmIdentity: executeIdentityConfirmationStep()
        case .runningApplications: executeRunningApplicationCheckStep()
        case .identified: break
        }
    }
    
    public func failedToIdentifyAsProvided(){
        self.failedToIdentify()
        
        // so the change is not shown while dismissing popup
        DispatchQueue.main.asyncAfter(deadline: .now() + 3){
            self.identifiedUser = ""
        }
    }
    
    public func requestIntructorApproval(){
        let request = StudentRequestManualApprovalApiRequest(query: .init(exam_id: self.exam_id))
        request.execute { (result:Result<StudentRequestManualApprovalApiRequest.Response, HttpClientError>) in
            
            switch result {
            case .success(let value):
                
                if value.message != "Success"{
                    self.showRequestInstructorApprovalButton = .visible
                    return
                }
                
                self.checkupVerificationStatus()
                
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
                
                self.showRequestInstructorApprovalButton = .visible
            }
        }
    }
    
    private func checkupVerificationStatus(){
        let request = StudentCheckVerificationStatusApiRequest(query: .init(exam_id: self.exam_id))
        request.execute { (result:Result<StudentCheckVerificationStatusApiRequest.Response, HttpClientError>) in
            
            switch result {
            case .success(let value):
                
                guard value.message == "Success", value.resource_bool == true else{
                    DispatchQueue.main.asyncAfter(deadline: .now() + 10){
                        self.checkupVerificationStatus()
                    }
                    return
                }
                
                self.showInstructorIdentityConfirmationDialog = true
                
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
                
                self.checkupVerificationStatus()
            }
        }
    }
    
    // MARK: Callbacks
    
    public var capturedPhoto:(()->NSImage?)?
    
    // MARK: - API Requests
    
    private func executeGetStartedStep(){
        currentStep = .face
    }
    
    private func executeFaceIdentificationStep(){
        
        isLoading.toggle()

        guard
            let photo = capturedPhoto?(),
            let base64ImageString = photo.base64String
        else {
            print("Can't get captured photo")
            return
        }

        let request = StudentIdentificationStep1ApiRequest(query: .init(image: base64ImageString))
        request.execute { (result:Result<StudentIdentificationStep1ApiRequest.Response, HttpClientError>) in
            
            self.isLoading.toggle()
            
            switch result {
            case .success(let value):
                self.identifiedUser = value.resource_str
                
                if self.identifiedUser == ""{
                    self.failedToIdentify()
                    self.showIdentificationFailureDialog = true
                    return
                }
                
                self.currentStep = .confirmIdentity
                self.showIdentityConfirmationDialog = true
                
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
    
    private func executeIdentityConfirmationStep(){
        currentStep = .runningApplications
    }
    
    private func executeRunningApplicationCheckStep(){
        
        isLoading.toggle()

        let service = RunningApplicationService.init()
        let runningApplications = service
            .execute()
            .compactMap(\.name)
        
        let request = StudentIdentificationStep3ApiRequest(query: .init(running_processes: runningApplications))
        request.execute { (result:Result<StudentIdentificationStep3ApiRequest.Response, HttpClientError>) in
            
            self.isLoading.toggle()
            
            switch result {
            case .success(let value):
                self.runningApplicationsNeedsCheck = false
                self.blockingApplications = value.resource_array
                
            case .failure(let error):
                print("Can't verify running applications")
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
    
    public func leaveExam(){

        isLoading.toggle()
        
        let request = StudentLeaveExamApiRequest(query: .init(exam_id: exam_id))
        request.execute { (result:(Result<StudentLeaveExamApiRequest.Response, HttpClientError>)) in
            
            self.isLoading.toggle()
            
            switch result{
            case .success(let response):
                if response.message != "Success"{
                    print("Cannot leave exam")
                    return
                }
                
                self.leaveExamCommand()
                
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
    
    // MARK: - Private Helpers
    
    private var failedIdentificationTries = 0
    
    private func failedToIdentify(){
        
        // Three tries = 0 1 2 
        if failedIdentificationTries == 3 - 1{
            
            showRequestInstructorApprovalButton = .visible
            
            return
        }
        
        failedIdentificationTries = failedIdentificationTries + 1
    }
    
    private func leaveExamCommand(){
        NotificationCenter
            .default
            .post(name: .pageRoutingNotification, object: PageRoute.Examination)
    }
}
