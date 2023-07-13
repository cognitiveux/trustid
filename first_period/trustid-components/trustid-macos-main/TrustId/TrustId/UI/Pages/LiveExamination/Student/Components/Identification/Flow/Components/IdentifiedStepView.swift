//
//  IdentifiedStepView.swift
//  TrustId
//
//  Created by Adamos Adamou on 30/12/21.
//

import SwiftUI

struct IdentifiedStepView: View {
    
    @EnvironmentObject var viewModel:StudentIdentificationSubPageViewModel
    
    public var identifitationCompleted: ()->Void
    
    var body: some View {
        GeometryReader{ proxy in
            VStack(spacing:64){
                Image.init(systemName: "checkmark.circle.fill")
                    .resizable()
                    .aspectRatio(contentMode: .fit)
                    .frame(width: proxy.size.width/3, height: proxy.size.height/3)
                    .foregroundColor(TrustIdPalette.green)
                
                VStack(spacing:32){
                    Text("You have been identified as \(viewModel.identifiedUser)")
                        .font(.custom("Roboto", size: 20))
                    Text("When you are ready, start the examination")
                        .font(.custom("Roboto", size: 20))
                    Button("Start Examination"){
                        identifitationCompleted()
                    }
                    .font(.custom("Roboto", size: 13))
                    .buttonStyle(BlueButton())
                }
            }.frame(maxWidth:.infinity, maxHeight: .infinity)
        }
    }
}

struct IdentifiedStepView_Previews: PreviewProvider {
    static var previews: some View {
        IdentifiedStepView {
            // do nothing
        }.environmentObject(StudentIdentificationSubPageViewModel(exam_id: "-"))
    }
}
