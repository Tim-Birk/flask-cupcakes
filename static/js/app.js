const BASE_URL = 'http://localhost:5000/api'
class CupcakeList {
    constructor() {
        this.addForm = $("#add-cupcake-form")
        this.list = $("#cupcake-list")

        this.addForm.on("submit", this.handleSubmit.bind(this))
    }

    async handleSubmit(evt) {
        evt.preventDefault()
        const flavor = $("#flavor").val()
        const size = $("#size").val()
        const image = $("#image").val()
        const rating = $("#rating").val()

        const cupcake = {
            flavor,
            size,
            image,
            rating
        }

        await axios.post(`${BASE_URL}/cupcakes`, cupcake)

        $("#flavor").val("")
        $("#size").val("small")
        $("#image").val("")
        $("#rating").val("")
        this.generateList()
    }
    async getCupcakes() {
        const response = await axios.get(`${BASE_URL}/cupcakes`)
        return response.data.cupcakes

    }
    async generateList() {
        this.list.empty()

        const cupcakes = await this.getCupcakes()

        cupcakes.forEach(c => {
            const div = $(`
            <div class="col col-md-6 col-lg-4 mb-3 d-flex justify-content-center" data-id="${c.id}">
                <div class="cupcake-container" style="width: 16rem;">
                    <a href='/cupcakes/${c.id}'>
                        <img src="${c.image}" class="card-img-top img-fluid" alt="${c.flavor} cupcake">
                    </a>
                    <div class="card-body">
                        <p class="card-text text-center">${c.flavor}</p>
                    </div>
                </div>
            </div>
            `)
            this.list.append(div)
        })
    }
}