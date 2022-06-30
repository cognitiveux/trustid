//
//  IdentificationStatusView.swift
//  TrustId
//
//  Created by Adamos Adamou on 14/12/21.
//

import SwiftUI

struct IdentificationStatusView: View {
    
    @EnvironmentObject var viewModel:StudentIdentificationSubPageViewModel
    
    var body: some View {
        VStack(spacing:32){
            VStack(spacing:16){
                Text("Identification & Verification Process")
                    .font(.custom("Roboto", size: 17))
                    .bold()
                    .frame(maxWidth:.infinity, alignment: .leading)
                
                VStack(alignment:.leading, spacing:16){
                    makeStepRow(1, text: "Face-based identification")
                    makeStepRow(2, text: "Checkup for third-party applications")
                }
                .frame(maxWidth:.infinity, alignment: .leading)
            }
                
            Text(identityVerificationMessage)
                .font(.custom("Roboto", size: 16))
                .foregroundColor(isIdentified ? TrustIdPalette.green : TrustIdPalette.red)
                .frame(maxWidth:.infinity, alignment: .center)
        }
    }
    
    private func makeStepRow(_ number:Int, text:String) -> some View{
        HStack(spacing:32){
            Text("Step \(number)")
                .font(.custom("Roboto", size: 13))
            Text(text)
                .font(.custom("Roboto", size: 13))
                .lineLimit(2)
        }
        .foregroundColor(calculateStepRowForegroundColor(number))
    }
    
    private func calculateStepRowForegroundColor(_ number:Int) -> Color{
        
        if number > currentStepNumber{
            return TrustIdPalette.stepGray
        }
        
        if number == currentStepNumber{
            return .black
        }
        
        return TrustIdPalette.green
    }
    
    private var identityVerificationMessage:String{
        return isIdentified
            ? "Identity Verification Completed"
            : "Identity Verification Pending"
    }
    
    private var currentStepNumber:Int{
        switch viewModel.currentStep{
        case .getStarted: return 0
        case .face, .confirmIdentity: return 1
        case .runningApplications: return 2
        case .identified: return 3
        }
    }
    
    private var isIdentified:Bool{
        if case .identified = viewModel.currentStep{
            return true
        }
        return false
    }
}

struct IdentificationStatusView_Previews: PreviewProvider {
    static var previews: some View {
        IdentificationStatusView()
            .environmentObject(StudentIdentificationSubPageViewModel(exam_id: "-"))
    }
}
