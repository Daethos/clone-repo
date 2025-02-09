<script lang="ts">
    import { onMount } from "svelte";
    import { Button } from "$lib/components/ui/button";
    type Item = {
        description: string;
        quantity: number;
    };
    type Order = {
        id: number;
        items: Item[] | [];
    };
    let input = $state("");
    let orders = $state<Order[]>([
        { id: 1, items: [{description: "Burger", quantity: 2}, {description: "Fries", quantity: 1}] },
        { id: 2, items: [{description: "Burger", quantity: 1}, {description: "Fries", quantity: 1}, {description: "Drink", quantity: 1}] },
        { id: 3, items: [{description: "Burger", quantity: 2}, {description: "Fries", quantity: 2}, {description: "Drink", quantity: 2}] }
    ]);
    let totals = $derived({
        burgers: orders.flatMap((order) => order.items)
        .filter((item) => item.description === "Burger")
        .reduce((sum, item) => sum + item.quantity, 0),
        fries: orders.flatMap((order) => order.items)
        .filter((item) => item.description === "Fries")
        .reduce((sum, item) => sum + item.quantity, 0),
        drinks: orders.flatMap((order) => order.items)
        .filter((item) => item.description === "Drink")
        .reduce((sum, item) => sum + item.quantity, 0),
    });
    let backendMessage = $state('Connecting to Order Mate!');

    onMount(async () => {
        const response = await fetch('http://127.0.0.1:8000/api/test');
        const data = await response.json();
        setTimeout(() => {
            backendMessage = data.message;
        }, 1000);
    });

    async function submitOrder() {
        // const body = { request: input };
        const response: {message:string; items:Item[] | number} = { message: "ORDER", items: [{description: "Burger", quantity: 2}, {description: "Fries", quantity: 1}] }
        // const response: {message:string; items:Item[] | number} = { message: "CANCEL", items: orders.length };
        console.log(response, "Response?")
        if (response.message === "ORDER") {
            const newOrder: Order = {
                id: orders.length + 1,
                items: response.items as Item[],
            };
            orders = [...orders, newOrder];
        } else if (response.message === "CANCEL") {
            const orderId = response.items as number;
            orders = orders.filter((order) => order.id !== orderId);
        };
        input = "";
        // const response = await fetch('http://127.0.0.1:8000/api/order', {
        //     method: "POST",
        //     headers: { "Content-Type": "application/json" },
        //     body: JSON.stringify(body),
        // });
        // console.log(response, "Response?")
        // if (!response.ok) {
        //     const errorData = await response.json();
        //     console.warn("Error:", errorData);
        // } else {
        //     const responseData = await response.json();
        //     console.log("Success:", responseData);
        //     if (responseData.message === "ORDER") {
        //         const newOrder = {
        //             id: orders.length + 1,
        //             items: responseData.items,
        //         };
        //         orders = [...orders, newOrder];
        //     } else if (responseData.message === "CANCEL") {
        //         const orderId = responseData.items;
        //         orders = orders.filter((order) => order.id !== orderId);
        //     };
        // };
    };

</script>
<main class='dark'>
    <div class="p-4 max-w-2xl mx-auto">
        <h1 class="text-2xl font-bold mb-4">{backendMessage}</h1>
        <h2 class="mb-4">Current Order Total</h2>
        <div class="grid grid-cols-3 gap-4 mb-8">
            <div class="border card mx-auto p-10 rounded-lg shadow-md">
                <h2 class="text-lg font-semibold">Burgers</h2>
                <p class="text-3xl font-bold">{totals.burgers}</p>
            </div>
            <div class="border card mx-auto p-10 rounded-lg shadow-md">
                <h2 class="text-lg font-semibold">Fries</h2>
                <p class="text-3xl font-bold">{totals.fries}</p>
            </div>
            <div class="border card mx-auto p-10 rounded-lg shadow-md">
                <h2 class="text-lg font-semibold">Drinks</h2>
                <p class="text-3xl font-bold">{totals.drinks}</p>
            </div>
        </div>
        <div class="flex gap-2 mb-4">
      <input
      bind:value={input}
      type="text"
      placeholder="Enter your order or cancel request"
      class="flex-1 p-2 border rounded"
      />
      <Button on:click={() => submitOrder()}>Place Request</Button>
    </div>
    
    <p class="mb-4">Order History: {orders.length}</p>
    <div class="space-y-2">
        {#each orders as order}
        <div class="p-4 border rounded">
            <p class="font-bold">Order #{order.id}</p>
            <ul class="list-disc pl-5">
                {#each order.items as item}
                
                <li>{item.quantity}x {item.description}</li>
                {/each}
            </ul>
            </div>
            {/each}
        </div>
    </div>
</main>;