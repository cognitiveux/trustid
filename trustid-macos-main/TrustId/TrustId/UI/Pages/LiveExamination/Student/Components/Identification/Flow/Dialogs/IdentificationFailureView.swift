//
//  IdentificationFailureView.swift
//  TrustId
//
//  Created by Adamos Adamou on 24/1/22.
//

import SwiftUI

struct IdentificationFailureView: View {
    
    @EnvironmentObject var viewModel:StudentIdentificationSubPageViewModel
    
    public let resetCapturedPhoto: ()->Void
    
    var body: some View {
        
        VStack(spacing:32){
            
            VStack(spacing:32){
                Text("We were not able to identify you")
                    .font(.custom("Roboto", size: 20))
                
                Text("Please retry capture")
                    .font(.custom("Roboto", size: 17))
            }
            HStack{
                Button("Dismiss") {
                    viewModel.showIdentificationFailureDialog = false
                    resetCapturedPhoto()
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

struct IdentificationFailureView_Previews: PreviewProvider {
    static var previews: some View {
        IdentificationFailureView(){
            // do nothing
        }
        .environmentObject(StudentIdentificationSubPageViewModel(exam_id: "-"))
        .preferredColorScheme(.light)
    }
}
