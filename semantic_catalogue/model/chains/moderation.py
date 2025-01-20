from langchain.chains import OpenAIModerationChain

moderate = OpenAIModerationChain()

if __name__ == "__main__":
    test_input = "Helpful outputs."
    test_out = moderate.invoke({"input": test_input})
    print(test_out)
