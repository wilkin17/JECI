import gradio as gr
import numpy as np
import matplotlib.pyplot as plt

def logisticregression(a_in,epoch_in,progress=gr.Progress()):
    #### generate random data-set ####

    #np.random.seed(0) # set random seed (optional)

    ## set mean and covariance of our datasets
    mean1 = [20,35]
    cov1 = [[100,100],[-100,100]] 
    mean2 = [60,70] 
    cov2 = [[100,100],[100,-100]] 

    ## concatenate values to set x values for datasets
    x1, x2 = np.random.multivariate_normal(mean1, cov1, 100).T
    x_1, x_2 = np.random.multivariate_normal(mean2, cov2, 100).T
    x1 = (np.concatenate((x1, x_1), axis=0))/10
    x2 = (np.concatenate((x2, x_2), axis=0))/10

    ## set y values of datasets
    y1 = np.zeros(100) # y[0:100] is zero dataset (dataset we want our decision boundary to be above)
    y2 = np.ones(100) # y[101:200] is one dataset (dataset we want our decision boundary to be below)
    y = np.concatenate((y1, y2), axis=0) # combine datasets into one term

    w = np.matrix([(np.random.rand())/100,(np.random.rand())+0.0001/100]) # begin weights at random starting point
    b = np.matrix([np.random.rand()]) # begin bias term at random starting point
    wb = np.concatenate((b, w), axis=1) # combine w and b into one weight term
    print('f = b + x1*w1 + x2*w2')
    print('Starting weights:', 'f = ', wb[0,0],'+ x1', wb[0,1], '+ x2' , wb[0,2])

    #a = 0.009 # learning rate
    a = a_in;
    #epoch = 1000 # number of training iterations
    epoch = epoch_in;

    loss = np.empty([epoch]) # term to store all loss terms for plotting
    iterat = np.empty([epoch]) # term to store all epoch numbers to be plotted vs loss
    for n in range (epoch):
        iterat[n] = n

    for p in progress.tqdm(range(epoch), desc="Calculating Loss"):
        L, J = np.matrix([[0.0, 0.0, 0.0]]), 0.0 # reset gradient (∂J(w)/∂w) and loss for each epoch
        #### Code the equations to solve for the loss and to update 
        #### the weights and biases for each epoch below. 
        
        #### Hint: you will need to use the for loop below to create a summation to solve 
        #### for wb and J (loss) for each epoch. xj has been given as a starting point.
        for i in range(len(x1)):
            xj = np.matrix([1,x1[i],x2[i]])
        
            # y_hat = (y_hat or h_w(x) expression)
            y_hat = (1 / (1 + np.exp(-wb * xj.T)))
            # J = (cost function, also referred to as L)
            J =  (y[i] * np.log10(y_hat)) + ((1-y[i]) * np.log10(1-y_hat)) 
            # d_J = (∂J(w)/∂w function, equation can be solved with information on slide 27)
            d_J = (y_hat-y[i])*xj
            # wb = (weight updating equation)
            wb = wb - (a * d_J)
            
        loss[p] = J
        J_out = J[0,0];
        if ((p % 100) == 0):
            print('loss:', J[0,0],'  Gradient (∂J(w)/∂w) [[b, w1, w2]]:',L[0])
    print('Updated weights:', 'f = ', wb[0,0],'+ x1', wb[0,1], '+ x2' , wb[0,2])
    
    ## Plot decision boundary and data
    fig1 = plt.figure()
    plt.plot(x1[1:100],x2[1:100],'x', x1[101:200], x2[101:200],'x') # plot random data points
    plt.plot(x1, -(x1*wb[0,1] + wb[0,0])/wb[0,2] , linestyle = 'solid') # plot decision boundary
    plt.axis('equal')
    plt.xlabel('x1')
    plt.ylabel('x2')
    plt.title('Decision Boundary')

    ## Plot training loss v epoch
    fig2 = plt.figure()
    plt.plot(iterat[100:],loss[100:],'x')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.title('Training Loss v Epoch')

    #plt.show()

    return J_out, fig1, fig2 # return loss and both plots

with gr.Blocks() as demo:
    gr.Markdown(
    """
    # Logistic Regression
    Adjust sliders for learning rate and epochs to see how it changes the loss for a logistic regression function!
    """)
    with gr.Row():
        inp = [gr.Slider(label="Learning Rate",value=0.009,maximum=0.01,minimum=0.001,step=0.0005),gr.Slider(label="Epochs (integer)",value=1000,maximum=5000,minimum=1,step=1)]
    with gr.Row():
        out = gr.Textbox(label="Loss")
    with gr.Row():
        plot1 = gr.Plot(min_width=170)
        plot2 = gr.Plot(min_width=180)
    with gr.Row():
        btn = gr.Button("Run")
    btn.click(fn=logisticregression, inputs=inp, outputs=[out,plot1,plot2])

demo.queue().launch()
