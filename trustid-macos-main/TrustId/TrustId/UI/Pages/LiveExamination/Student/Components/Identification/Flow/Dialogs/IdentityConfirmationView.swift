//
//  IdentityConfirmationView.swift
//  TrustId
//
//  Created by Adamos Adamou on 14/12/21.
//

import SwiftUI

struct IdentityConfirmationView: View {
    
    @EnvironmentObject var viewModel:StudentIdentificationSubPageViewModel
    
    @State private var authenticationItemMaxWidth:CGFloat?
    
    public let resetCapturedPhoto: ()->Void
    
    var body: some View {
        
        VStack(spacing:64){
            
            Text("We identified you as \(viewModel.identifiedUser)")
                .font(.custom("Roboto", size: 20))
            
            HStack{
                Button("Proceed to Step 2") {
                    viewModel.showIdentityConfirmationDialog = false
                    viewModel.executeStep()
                }
                .font(.custom("Roboto", size: 13))
                .buttonStyle(BlueButton(width:authenticationItemMaxWidth))
                .frame(width:authenticationItemMaxWidth)
                .overlay(DetermineWidth())

                Button("I am not \(viewModel.identifiedUser)"){
                    viewModel.showIdentityConfirmationDialog = false
                    viewModel.currentStep = .face
                    resetCapturedPhoto()
                    viewModel.failedToIdentifyAsProvided()
                }
                .font(.custom("Roboto", size: 13))
                .buttonStyle(RedButton(width:authenticationItemMaxWidth))
                .frame(width:authenticationItemMaxWidth)
                .overlay(DetermineWidth())
            }
            .onPreferenceChange(DetermineWidth.Key.self){
                authenticationItemMaxWidth = $0
            }
        }
        .frame(minWidth: 400)
        .padding(32)
        .background(Color.white)
    }
}

struct IdentityConfirmationView_Previews: PreviewProvider {
    static var previews: some View {
        IdentityConfirmationView(){
            // do nothing
        }
        .environmentObject(StudentIdentificationSubPageViewModel(exam_id: "-"))
        .preferredColorScheme(.light)
    }
}
