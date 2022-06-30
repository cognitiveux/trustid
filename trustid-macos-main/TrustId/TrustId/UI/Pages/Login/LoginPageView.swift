//
//  LoginPageView.swift
//  TrustId
//
//  Created by Adamos Adamou on 22/11/21.
//

import SwiftUI

extension NSTextField {
    open override var focusRingType: NSFocusRingType {
        get { .none }
        set { }
    }
}

struct LoginPageView: View {
    
    @StateObject private var viewModel = LoginPageViewModel()
    
    @State private var username = ""
    @State private var password = ""
    
    @State private var authenticationItemMaxWidth:CGFloat?
    @State private var authenticationItemMaxHeight:CGFloat?
    
    var body: some View {
        VStack {
            Spacer()
            organizationDetailsGroup
                .frame(width:350)
            Spacer()
            authenticationGroup
                .frame(width:400)
            Spacer()
            Spacer()
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
        .background(Color.white)
        .overlay(LoadingView(isLoading: viewModel.isLoading))
        .sheet(isPresented: $viewModel.showErrorDialog){
            ErrorView(message: viewModel.showErrorDialogMessage)
        }
    }
    
    private var organizationDetailsGroup: some View{
        VStack(alignment:.leading){
            HStack{
                Image("trustid-logo")
                    .resizable()
                    .aspectRatio(contentMode: .fit)
                HStack{
                    Image("eu")
                        .resizable()
                        .aspectRatio(contentMode: .fit)
                    Image("iky")
                        .resizable()
                        .aspectRatio(contentMode: .fit)
                }
                .frame(width: 75)
            }
            
            Text("Intelligent Student Identity Management for Higher Education Institutions")
                .font(.custom("Roboto", size: 11))
                .lineLimit(2)
                .foregroundColor(TrustIdPalette.buttonBlue)
        }
    }
    
    private var authenticationGroup: some View{
        VStack(spacing:16){
            VStack{
                TextField("Username", text: $username)
                    .font(.custom("Roboto", size: 13))
                    .padding(.horizontal, 16)
                    .frame(width:authenticationItemMaxWidth, height:authenticationItemMaxHeight)
                    .overlay(DetermineWidth())
                    .overlay(DetermineHeight())
                    .textFieldStyle(.plain)
                    .background(border)
                
                SecureField("Password", text: $password)
                    .font(.custom("Roboto", size: 13))
                    .padding(.horizontal, 16)
                    .frame(width:authenticationItemMaxWidth, height:authenticationItemMaxHeight)
                    .overlay(DetermineHeight())
                    .overlay(DetermineWidth())
                    .textFieldStyle(.plain)
                    .background(border)
            }
            
            Button("Login"){
                viewModel.login(with: username, and: password)
            }
            .font(.custom("Roboto", size: 13))
            .buttonStyle(BlueButton(width:authenticationItemMaxWidth, height: authenticationItemMaxHeight))
            .frame(width:authenticationItemMaxWidth, height:authenticationItemMaxHeight)
            .overlay(DetermineWidth())
            .overlay(DetermineHeight())
        }
        .onPreferenceChange(DetermineHeight.Key.self){
            authenticationItemMaxHeight = $0
        }
        .onPreferenceChange(DetermineWidth.Key.self){
            authenticationItemMaxWidth = $0
        }
    }
    
    var border: some View {
        RoundedRectangle(cornerRadius: 8)
            .strokeBorder(TrustIdPalette.buttonBlue, lineWidth: 1)
    }
}

struct LoginPageView_Previews: PreviewProvider {
    static var previews: some View {
        LoginPageView()
    }
}
