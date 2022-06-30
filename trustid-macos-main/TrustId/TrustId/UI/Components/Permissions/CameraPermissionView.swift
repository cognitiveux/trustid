//
//  CameraPermissionView.swift
//  TrustId
//
//  Created by Adamos Adamou on 21/1/22.
//

import SwiftUI

struct CameraPermissionView: View{
    
    @Binding public var isPresented:Bool
    
    var body: some View{
        VStack(spacing:32){
            VStack(spacing:32){
                Text("Please enable camera permission by following these steps")
                    .font(.custom("Roboto", size: 20))
                
                VStack(alignment: .leading, spacing:16){
                    makeSingleInstructionView(
                        "Go to",
                        "System Preferences -> Security & Privacy -> Privacy -> Camera"
                    )
                    makeSingleInstructionView(
                        "Tick",
                        "TrustId"
                    )
                }
            }
            .foregroundColor(.black)
            
            HStack{
                Button("Dismiss") {
                    isPresented = false
                }
                .font(.custom("Roboto", size: 13))
                .buttonStyle(BlueButton())
            }
        }
        .frame(width: 600)
        .padding(32)
        .background(Color.white)
    }
    
    private func makeSingleInstructionView(_ instructionText:String, _ instructionDetails:String) -> some View{
        HStack(spacing:8){
            Text(instructionText)
                .font(.custom("Roboto", size: 17))
                .bold()
            Text(instructionDetails)
                .font(.custom("Roboto", size: 17))
        }
    }
}

struct CameraPermissionView_Previews: PreviewProvider {
  
    static var previews: some View {
        CameraPermissionView(isPresented: .constant(false))
            .previewLayout(.sizeThatFits)
            .frame(width: 600, alignment: /*@START_MENU_TOKEN@*/.center/*@END_MENU_TOKEN@*/)
    }
}
