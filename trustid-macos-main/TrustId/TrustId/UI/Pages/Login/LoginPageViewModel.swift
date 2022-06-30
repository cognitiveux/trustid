//
//  LoginPageViewModel.swift
//  TrustId
//
//  Created by Adamos Adamou on 23/11/21.
//

import Foundation

final class LoginPageViewModel:ObservableObject{
    
    // MARK: Dependencies
    
    private var tokenService = AuthenticationTokenService.shared
    private var userService = UserService.shared
    
    // MARK: - Output
    
    @Published public var showErrorDialog = false
    @Published public var showErrorDialogMessage = "-"
    
    @Published public var isLoading = false
    
    // MARK: - Input
    
    public func login(with username:String, and password:String){
        
        if username.count == 0 || password.count == 0{
            self.showErrorDialogMessage = "Pleaser enter credentials"
            self.showErrorDialog.toggle()
            return
        }
        
        isLoading = true
        
        let request = LoginApiRequest(query: .init(email: username, password: password))
        request.execute { (result:Result<LoginApiRequest.Response, HttpClientError>) in
            
            self.isLoading = false
            
            switch result {
                
            case let .success(value):
                self.tokenService.access = value.resource_obj.access
                self.tokenService.refresh = value.resource_obj.refresh
                
                if let role = self.tokenService.userRole{
                    let userInfoTuple = self.tokenService.userNameSurname
                    self.userService.store(user: .init(name: userInfoTuple.name, surname: userInfoTuple.surname, type: role))
                    self.sendUserAuthenticatedEvent()
                } else {
                    print("access token expired/invalid")
                }

            case let .failure(error):
                print(error.localizedDescription)
                self.tokenService.access = nil
                self.tokenService.refresh = nil
                
                switch error{
                case .failed(_):
                    print("ApiError: -failed")
                    self.showErrorDialogMessage = "Request failed contact developer"
                    self.showErrorDialog.toggle()
                case .noData:
                    print("ApiError: -noData")
                    self.showErrorDialogMessage = "Request failed contact developer"
                    self.showErrorDialog.toggle()
                case .apiErrorResponse(let statusCode, let data):
                    print("ApiError: \(statusCode) \(data.message)")
                    self.showErrorDialogMessage = data.message
                    self.showErrorDialog.toggle()
                }
            }
        }
    }
}

extension LoginPageViewModel{
    
    private func sendUserAuthenticatedEvent(){
        NotificationCenter.default
            .post(name: .userAuthenticatedNotification, object: nil)
    }
}
