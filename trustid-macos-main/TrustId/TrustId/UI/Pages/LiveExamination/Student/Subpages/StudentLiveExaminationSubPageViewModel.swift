//
//  StudentLiveExaminationSubPageViewModel.swift
//  TrustId
//
//  Created by Adamos Adamou on 28/12/21.
//

import Foundation
import AppKit

final class StudentLiveExaminationSubPageViewModel:ObservableObject{
    
    // MARK: - Initiliser
    
    let exam_id:String
    
    init(exam_id:String){
        self.exam_id = exam_id
    }
    
    // MARK: - Output
    
    @Published public var isLoading = false
    
    // MARK: - Input
    
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
    
    public func executeMonitoringRequest(capturedImage:NSImage){
        
        guard let base64ImageString = capturedImage.base64String else {
            print("Can't get captured photo")
            return
        }
        
        self.isLoading.toggle()
        
        let ipService = IpAddressService.init()
        ipService.execute { ipAddress in
            self.executeApiRequest(image: base64ImageString, ip: ipAddress)
        }
    }
    
    // MARK: Internal
    
    private func executeApiRequest(image:String, ip:String){
        
        let service = RunningApplicationService.init()
        let runningApplications = service
            .execute()
            .compactMap(\.name)
        
        let request = StudentMonitoringApiRequest(
            query: .init(
                exam_id: self.exam_id,
                running_processes: runningApplications,
                ip_address: ip,
                image: image
            )
        )
        
        request.execute { (result:Result<StudentMonitoringApiRequest.Response, HttpClientError>) in
            
            self.isLoading.toggle()
            
            switch result {
            case .success(let value):
                print(value)
                
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
    
    private func leaveExamCommand(){
        NotificationCenter
            .default
            .post(name: .pageRoutingNotification, object: PageRoute.Examination)
    }
}
