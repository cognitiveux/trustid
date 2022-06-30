//
//  InstructorIdentityConfirmationView.swift
//  TrustId
//
//  Created by Adamos Adamou on 16/1/22.
//

import SwiftUI

struct InstructorIdentityConfirmationView: View {
        
    @EnvironmentObject var viewModel:StudentIdentificationSubPageViewModel
    
    var body: some View {
        VStack(spacing:32){
            
            VStack(spacing:32){
                Text("Instructor has manually approved you")
                    .font(.custom("Roboto", size: 20))
                
                Text("Please proceed to next step")
                    .font(.custom("Roboto", size: 17))
            }
            
            HStack{
                Button("Continue") {
                    viewModel.showInstructorIdentityConfirmationDialog = false
                    viewModel.currentStep = .runningApplications
                }
                .font(.custom("Roboto", size: 13))
                .buttonStyle(BlueButton())
            }
        }
        .frame(minWidth: 400)
        .padding(32)
        .background(Color.white)
    }
}

struct InstructorIdentityConfirmationView_Previews: PreviewProvider {
    static var previews: some View {
        InstructorIdentityConfirmationView()
            .environmentObject(StudentIdentificationSubPageViewModel(exam_id: "-"))
            .preferredColorScheme(.light)
    }
}
