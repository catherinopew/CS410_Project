async function initiateTask(client_id, server_url, amazon_url) {
    const response = await fetch(server_url + '/send_request', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            client_id: client_id,
            url: amazon_url
        })
    });

    const data = await response.json();
    return data.message.task_id;
}

async function checkTaskStatus(taskId, client_id, server_url) {
    let taskCompleted = false;
    let result = null;

    while (!taskCompleted) {
        const response = await fetch(server_url + '/get_response', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                client_id: client_id,
                task_id: taskId
            })
        });

        const data = await response.json();

        if (data.message !== "the task is in progress") {
            taskCompleted = true;
            result = data;
        } else {
            await new Promise(resolve => setTimeout(resolve, 1000));
        }
    }

    return result;
}

async function main() {
    let client_id = "103045";
    let amazon_url = "https://www.amazon.com/Nike-Womens-Running-Metallic-Numeric_12/dp/B01AMT0EYU/ref=cm_cr_arp_d_product_top?ie=UTF8";
    let server_url = "http://ec2-52-90-81-216.compute-1.amazonaws.com:8080";

    console.log('Starting the process...')
    const startTime = Date.now();

    try {
        const taskId = await initiateTask(client_id, server_url, amazon_url);
        const taskResult = await checkTaskStatus(taskId, client_id, server_url);

        const endTime = Date.now();
        const timeTaken = endTime - startTime;
        console.log(`Fetch completed in ${timeTaken / 1000} seconds.`);
        console.log(taskResult);
    } catch (error) {
        console.error('An error occurred:', error);
    }
}

main();
